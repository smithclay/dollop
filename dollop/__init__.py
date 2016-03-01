__version__ = '1.0.0'

from troposphere import Ref, Template, Parameter, Output, GetAtt, Tags
from .cloudformationhelper import CloudFormationHelper


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





