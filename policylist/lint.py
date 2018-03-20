import sys,os
from policylist import policy
from policylist import constants

# Linting script.
# Loads policy file, and ensure that it's well-formed.

def lint_string(data):
    return policy.deserialize_config(data)

def lint(filename=constants.POLICY_LOCAL_FILE):
    return config_from_file(filename)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        lint()
    else:
        lint(sys.argv[1])

