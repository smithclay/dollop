## dollop: an easy way to create simple servers in the cloud
<img src="http://i.imgur.com/FmKOhdT.jpg" alt="Dollop" height="260px"></img>

Dollop is a thin python wrapper around [AWS CloudFormation](https://aws.amazon.com/cloudformation/) built using troposphere. It's an easy way to create simply-configured EC2 instances for testing or development purposes.

For more complex EC2 automation scenarios, look into AWS OpsWorks or rolling your own Puppet or Chef environment.

Other IaaS providers might be supported in the future. For now it's just Amazon Web Services (AWS).

### Requirements

* Python 2.7
* Mac or Linux
* Amazon Web Services Account

### Example

Coming soon.

### Setup on AWS

An SSH key pair is needed to SSH into the hosts that dollop creates. It's easy to create one using the [AWS CLI](https://aws.amazon.com/cli/) tools:

```
aws ec2 create-key-pair --key-name devenvkey --query 'KeyMaterial' --output text > ~/.ssh/devenvkey.pem
```

It's then possible to use that key pair to SSH into the dollop-generated host:

```
ssh -i ~/.ssh/devenvkey.pem ubuntu@your-ec2-host
```

### Troubleshooting on AWS

* Look at the CloudFormation output logs
* Look at the output in `/var/logs` on the EC2 instance

### External Documentation

* http://docs.aws.amazon.com/cli/latest/userguide/tutorial-ec2-ubuntu.html
* https://github.com/cloudtools/troposphere
* https://docs.docker.com/engine/installation/cloud/cloud-ex-aws/
* http://airbnb.io/cloud-maker/