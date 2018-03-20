import datetime
import itertools
import logging
import mock
import unittest

import policy

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


test_json = '{\
    "author": "Electronic Frontier Foundation",\
        "comment": "Sample policy configuration file",\
        "expires": 1404677353,\
        "timestamp": 1401093333,\
        "tls-policies": {\
            ".valid.example-recipient.com": {\
                "min-tls-version": "TLSv1.1",\
                    "mode": "enforce",\
                    "mxs": [".valid.example-recipient.com"],\
                    "require-valid-certificate": true,\
                    "tls-report": "https://tls-rpt.example-recipient.org/api/report"\
            }\
        }\
    }'


class TestPolicy(unittest.TestCase):
    """Test Policy config
    """

    def test_basic(self):
        mock_open = mock.mock_open(read_data=test_json)
        conf = policy.Config()
        with mock.patch('policy.open', mock_open):
            conf.load()
        self.assertEqual(conf.author, "Electronic Frontier Foundation")
        print conf.tls_policies
        self.assertEqual(conf.tls_policies, {'.valid.example-recipient.com': {
                'min-tls-version': 'TLSv1.1',
                'mode': 'enforce',
                'mxs': ['.valid.example-recipient.com'],
                'require-valid-certificate': True,
                'tls-report': 'https://tls-rpt.example-recipient.org/api/report',
            }})

if __name__ == '__main__':
    unittest.main()
