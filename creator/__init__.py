__version__ = '1.0.0'

from troposphere import Base64, Ref, Join, Template, Parameter, Output, GetAtt, Tags
from troposphere import cloudformation
import troposphere.ec2 as ec2

# *Ubuntu* 14.04 AMI Image in us-west
IMAGE_ID = 'ami-9abea4fb'
SSH_PORT = 22


class Tub(object):
    """
    Used to group dollops together. Corresponds to an
    AWS CloudFormation stack.
    """

    def __init__(self, description):
        self.description = description
        self.dollops = []

    def add_dollop(self, dollop):
        self.dollops.append(dollop)

    def to_cloudformation_template(self):
        t = Template()
        t.description = self.description

        for d in self.dollops:
            d.to_cloudformation_template(t)
        return t


class Dollop(object):
    """
    Dollops can be servers or other resources. They belong
    to a single Tub.
    """

    def __init__(self, name):
        self.name = name

    def to_cloudformation_template(self, base_template):
        raise 'Must implement AWS CloudFormation Template Generation'


class CloudFormationHelper(object):
    """
    A DollopServer represents an instance on an operating system
    running on infrastructure.
    """

    @classmethod
    def create_security_group_rules(cls, ports):
        rules = []
        for p in ports:
            rules.append(ec2.SecurityGroupRule(
                IpProtocol='tcp',
                FromPort=p,
                ToPort=p,
                CidrIp='0.0.0.0/0'
            ))
        return rules

    @classmethod
    def create_user_data(cls, file_contents, instance_name):
        lines = file_contents.splitlines()
        lines = [l + '\n' for l in lines]

        lines.extend(('cfn-init -s \'',
                      Ref('AWS::StackName'), '\' -r {0} --region '.format(instance_name),
                      Ref('AWS::Region'),
                      ' -c default\n'
                      ))

        return Base64(Join('', lines))


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
    def to_cloudformation_template(self, base_template):
        instance = ec2.Instance(self.name)
        instance.InstanceType = 't2.nano'
        instance.ImageId = IMAGE_ID

        base_template.add_resource(instance)

        if self.bootstrap_file_contents:
            instance.UserData = CloudFormationHelper.create_user_data(self.bootstrap_file_contents, self.name)
            instance.Metadata = cloudformation.Metadata(
                cloudformation.Init(
                    cloudformation.InitConfigSets(
                        default=['metadata']
                    ),
                    metadata=cloudformation.InitConfig(
                        commands={
                            'write_metadata': {
                                'command': 'echo "$DOLLOP_VERSION" > dollop_init.txt',
                                'env': {
                                    'DOLLOP_VERSION': __version__
                                },
                                'cwd': '~'
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
