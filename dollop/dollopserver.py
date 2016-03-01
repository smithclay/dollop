from troposphere import cloudformation, Ref, Output, GetAtt, Parameter, Tags, Join
import troposphere.ec2 as ec2
from troposphere.constants import SSH_PORT
from .cloudformationhelper import CloudFormationHelper
from . import __version__, Dollop

# *Ubuntu* 14.04 AMI Image in us-west
# TODO: have a list of ubuntu images ready to go.
# TODO: make it easier to write commands

IMAGE_ID = 'ami-9abea4fb'


class DollopServer(Dollop):
    """
    A DollopServer represents an instance on an operating system
    running on infrastructure.
    """

    DefaultTag = 'ops.dollop.resource.ec2'

    def __init__(self, name):
        super(DollopServer, self).__init__(name)

        self.open_ports = [SSH_PORT]
        self.outputs = []
        self.commands = []
        self.bootstrap_file_contents = ''

    # TODO: Extract into CloudFormation helper class
    # TODO: Better way to handle tagging
    def to_cloudformation_template(self, base_template):
        instance = ec2.Instance(self.name)
        instance.InstanceType = 't2.nano'
        instance.ImageId = IMAGE_ID

        base_template.add_resource(instance)

        if self.bootstrap_file_contents:
            newrelic_license_param = base_template.add_parameter(Parameter(
                "NewRelicLicenseKey",
                Description="Value of your New Relic License Key",
                Type="String",
            ))

            instance.UserData = CloudFormationHelper.create_user_data(self.bootstrap_file_contents, self.name)
            instance.Metadata = cloudformation.Metadata(
                cloudformation.Init(
                    cloudformation.InitConfigSets(
                        default=['new_relic']
                    ),
                    new_relic=cloudformation.InitConfig(
                        commands={
                            'write_dollop_version': {
                                'command': 'echo "$DOLLOP_VERSION" > dollop_init.txt',
                                'env': {
                                    'DOLLOP_VERSION': __version__
                                },
                                'cwd': '~'
                            },
                            'configure_new_relic': {
                                'command': Join('',
                                                ['nrsysmond-config --set license_key=', Ref(newrelic_license_param)])
                            }
                        },
                        services={
                            'sysvinit': {
                                'newrelic-sysmond': {
                                    'enabled': 'true',
                                    'ensureRunning': 'true'
                                }
                            }
                        }
                    )
                )
            )
        if SSH_PORT in self.open_ports:
            keyname_param = base_template.add_parameter(Parameter(
                "EC2KeyPair",
                Description="Name of an existing EC2 KeyPair to enable SSH access to the instance",
                Type="AWS::EC2::KeyPair::KeyName",
            ))

            security_group = base_template.add_resource(ec2.SecurityGroup(
                'DollopServerSecurityGroup',
                GroupDescription='Dollop-generated port access rules for an EC2 instance',
                SecurityGroupIngress=CloudFormationHelper.create_security_group_rules(self.open_ports),
                Tags=Tags(Name='ops.dollop.resource.sg'))
            )
            instance.KeyName = Ref(keyname_param)
            instance.SecurityGroups = [Ref(security_group)]

        # Template Output
        base_template.add_output([
            Output(
                "InstanceId",
                Description="InstanceId of the newly created EC2 instance",
                Value=Ref(instance),
            ),
            Output(
                "AZ",
                Description="Availability Zone of the newly created EC2 instance",
                Value=GetAtt(instance, "AvailabilityZone"),
            ),
            Output(
                "PublicIP",
                Description="Public IP address of the newly created EC2 instance",
                Value=GetAtt(instance, "PublicIp"),
            ),
            Output(
                "PrivateIP",
                Description="Private IP address of the newly created EC2 instance",
                Value=GetAtt(instance, "PrivateIp"),
            ),
            Output(
                "PublicDNS",
                Description="Public DNS Name of the newly created EC2 instance",
                Value=GetAtt(instance, "PublicDnsName"),
            ),
            Output(
                "PrivateDNS",
                Description="Private DNS Name of the newly created EC2 instance",
                Value=GetAtt(instance, "PrivateDnsName"),
            ),
        ])
        instance.Tags = Tags(Name=DollopServer.DefaultTag)
        return base_template
