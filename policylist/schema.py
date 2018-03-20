from policylist import util

# JSON schema definitions.
# All in one place!

# Each schema definition (for a particular field) has three possible
# entries: `enforce`, `default`, and `required`.
# `enforce`  function that expects to return True when called on
#            the field; otherwise, `ConfigError` is raised.
# `default`  default value of this field, if it is not specified.
# `required` if True, then ConfigError is thrown if this field is not specified
#            and there is no default value.


TLS_VERSIONS = ('TLSv1', 'TLSv1.1', 'TLSv1.2', 'TLSv1.3')
ENFORCE_MODES = ('none', 'testing', 'enforce')

POLICY_SCHEMA = {
        'min-tls-version': {
            'enforce': util.enforce_in(TLS_VERSIONS),
            'default': 'TLSv1.2',
            },
        'mode': {
            'enforce': util.enforce_in(ENFORCE_MODES),
            'default': 'testing',
            },
        'mxs': util.enforce_list(util.enforce_type(unicode)),
        'tls-report': util.enforce_type(unicode),
        'require-valid-certificate': util.enforce_type(bool),
        }

CONFIG_SCHEMA = {
        'author': util.enforce_type(unicode),
        'comment': util.enforce_type(unicode),
        'expires': {
            'enforce': util.enforce_valid_date,
            'required': True,
            },
        'policy-alias': {
            util.enforce_fields(util.enforce_object(POLICY_SCHEMA)),
        },
        'pinsets': {
            util.enforce_fields(util.enforce_list(util.enforce_type(unicode)))
        },
        'timestamp': {
            'enforce': util.enforce_valid_date,
            'required': True,
            },
        'tls-policies': util.enforce_fields(util.enforce_object(POLICY_SCHEMA)),
        }


