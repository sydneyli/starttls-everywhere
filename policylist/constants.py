import os

POLICY_REMOTE_URL = "https://raw.githubusercontent.com/sydneyli/starttls-everywhere/policy_api/test_rules/config.json"
POLICY_FILENAME = "rules.json"
POLICY_LOCAL_FILE = os.path.join(os.path.dirname(__file__), POLICY_FILENAME)
