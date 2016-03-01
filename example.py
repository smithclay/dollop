from dollop.dollopserver import DollopServer
from dollop import Tub

# Create a new stack with a single server
t = Tub('My Example Stack')
server_a = DollopServer('ServerA')
t.add_dollop(server_a)

# Have the server run a custom bootstrap script
server_a.bootstrap_file_contents = open('data/ubuntu_bootstrap_newrelic.sh').read()

# Write CloudFormation template to dish
json = t.to_cloudformation_template().to_json()
f = open('output.json', 'w')
f.write(json)

print 'wrote to output.json!'