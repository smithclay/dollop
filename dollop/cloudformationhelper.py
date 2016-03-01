from troposphere import Base64, Ref, Join
import troposphere.ec2 as ec2

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
    def create_user_data(cls, file_contents, instance_name, config_name='default'):
        lines = file_contents.splitlines()
        lines = [l + '\n' for l in lines]

        lines.extend(('cfn-init -s \'',
                      Ref('AWS::StackName'), '\' -r {0} --region '.format(instance_name),
                      Ref('AWS::Region'),
                      ' -c {0}\n'.format(config_name)
                      ))

        return Base64(Join('', lines))