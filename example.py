from dollop import DollopServer, Tub

# Create a new stack with a single server
t = Tub('My Example Stack')
server_a = DollopServer('ServerA')
server_a.bootstrap_file_contents = open('data/ubuntu_bootstrap.sh').read()
t.add_dollop(server_a)

# Write CloudFormation template to dish
json = t.to_cloudformation_template().to_json()
f = open('output.json', 'w')
f.write(json)
