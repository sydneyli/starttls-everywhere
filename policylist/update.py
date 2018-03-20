import os
import pycurl
import shutil
import StringIO

from policylist import policy
from policylist import constants

def _should_replace(old_config, new_config):
    return new_config['timestamp'] > old_config['timestamp']

def _get_remote_data(url):
    buf = StringIO.StringIO()
    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.WRITEFUNCTION, buf.write)
    curl.perform()
    curl.close()
    return buf.getvalue()

def update(remote_url=constants.POLICY_REMOTE_URL, filename=constants.POLICY_LOCAL_FILE):
    try:
        import pycurl
    except ImportError:
        raise Exception("Please install PycURL library.")
    data = _get_remote_data(remote_url)
    remote_config = policy.deserialize_config(data)
    local_config = policy.config_from_file(constants.POLICY_LOCAL_FILE)
    if _should_replace(local_config, remote_config):
        with open(constants.POLICY_LOCAL_FILE, 'w+') as handle:
            handle.write(data)

if __name__ == "__main__":
    update()
