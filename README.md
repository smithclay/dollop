## dollop: an easy way to create cloud servers

Dollop is a thin python wrapper around AWS CloudFormation. It's an easy way to create simply-configured EC2 instances for testing or development purposes.

For more complex EC2 automation scenarios, look into AWS OpsWorks or rolling your own Puppet or Chef environment.

Eventually other IaaS providers might be supported. For now it's just Amazon Web Services.

### Requirements

* Python 2.7
* Mac or Linux

### Setup on AWS

An SSH key pair is needed to SSH into the hosts that dollop creates. It's easy to create one using the AWS CLI tools:

```
aws ec2 create-key-pair --key-name devenvkey --query 'KeyMaterial' --output text > ~/.ssh/devenvkey.pem
```

### Troubleshooting on AWS

* Look at the CloudFormation output logs
* Look at the output in `/var/logs` on the EC2 instance

### External Documentation

* http://docs.aws.amazon.com/cli/latest/userguide/tutorial-ec2-ubuntu.html
* https://github.com/cloudtools/troposphere