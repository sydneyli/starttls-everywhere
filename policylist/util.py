from functools import partial
import datetime
import json
from dateutil import parser # Dependency: python-dateutil

# Duck typing because it's important that the policies are
# well-formed. Until we get a better type system.

class ConfigError(ValueError):
    def __init__(self, message):
        super(self.__class__, self).__init__(message)

def enforce_in(possible):
    return lambda val: val in possible

def _parse_valid_date(date):
    if isinstance(date, int):
        try:
            return datetime.datetime.fromtimestamp(date)
        except (TypeError, ValueError):
            raise ConfigError("Invalid date: {}".format(date))
    try: # Fallback: try to parse a string-like
        return parser.parse(date)
    except (TypeError, ValueError):
        raise ConfigError("Invalid date: {}".format(date))

def enforce_valid_date(date):
    return isinstance(date, datetime.datetime)

def enforce_type(type):
    return lambda val: isinstance(val, type)

def enforce_list(func):
    return lambda l: isinstance(l, list) and all(func(val) for val in l)

def enforce_object(spec):
    return lambda val: isinstance(val, dict) and check_schema(val, spec) is not None

def enforce_fields(func):
    return lambda obj: all(func(value) for value in obj.values())

def _get_properties(schema):
    if isinstance(schema, dict):
        enforce = schema['enforce'] if 'enforce' in schema else None
        default = schema['default'] if 'default' in schema else None
        required = schema['required'] if 'required' in schema else False
        return enforce, default, required
    else:
        return schema, None, None

def check_schema(obj, schema):
    for field, subschema in schema.iteritems():
        enforce, default, required = _get_properties(subschema)
        if field not in obj.keys():
            if required and default is None:
                raise ConfigError("Field {0} is required!".format(field))
            obj[field] = default
            continue
        if enforce is not None and not enforce(obj[field]):
            raise ConfigError("Field '{0}: {1}' is invalid.".format(field, obj[field]))
    return True

# Extra JSON decoding/encoding helpers

# Encoder
class ConfigEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%S%z')
        return json.JSONEncoder.default(self, obj)

# Decoder
def _config_hook(obj):
    if 'expires' in obj:
        obj['expires'] = _parse_valid_date(obj['expires'])
    if 'timestamp' in obj:
        obj['timestamp'] = _parse_valid_date(obj['timestamp'])
    return obj

