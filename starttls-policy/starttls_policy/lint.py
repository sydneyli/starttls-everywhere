""" Util for updating local version of the policy file. """

import os
import json
import requests

from starttls_policy import constants
from starttls_policy import policy

def _should_replace(old_config, new_config):
    return new_config.timestamp > old_config.timestamp

def _get_remote_data(url):
    return requests.get(url).text

def _pretty_print_relevant_lines(contents, line, column, context=2):
    """ Returns empty string if can't find relevant line/column.
    Otherwise returns a nicely formatted string containing `line` in
    `contents` +/- `context`, assuming both line and column are zero-indexed.
    For instance, for the following content:
        { "a": "b"
          "c": 3,
          "d": "x" }
    called on line 1, column 2, the result would look like:
        1: { "a": "b"
        2:   "c": 3,
        -----^
        3:   "d": "x" }
    Note that the printed lines are 1-indexed.
    """
    result = "\n\n"
    content_lines = contents.splitlines()
    if line < 0 or line > len(content_lines):
        return ""
    min_line = max(0, line - context)
    max_line = min(len(content_lines) - 1, line + context)
    linenum_width = len(str(max_line+1))
    linenum_format = "{0: <" + str(linenum_width + 2) + "}"
    for lineno in range(min_line, max_line + 1):
        prefix = linenum_format.format(str(lineno+1) + ":")
        result += prefix + content_lines[lineno] + "\n"
        if lineno == line:
            result += ("-" * (column + len(prefix))) + "^\n"
    return result

def _describe_json_decode_error(contents, err):
    """
    This is a python2/python3 compatible way to describe the JSON error.
    The fmt string is one of the two:
        {0}: line {1} column {2} (char{3})
        {0}: line {1} column {2} - line {3} column {4} (char {5} - {6})
    If we can't find the line/column numbers since the message is not well-formed,
    just raise the original error message.

    For instance, for the following misformatted JSON:
        { "a": "b"
          "c": 3,
          "d": "x" }
    The following might be printed to stderr:
        1: { "a": "b"
        2:   "c": 3,
        -----^
        3:   "d": "x" }
    """
    errmsg = str(err)
    errmsg_words = str(err).strip().split()
    # if can't find line/column
    if "line" not in errmsg_words or "column" not in errmsg_words:
        raise err
    line_index = errmsg_words.index("line")
    column_index = errmsg_words.index("column")
    # if out of index
    if line_index + 1 >= len(errmsg_words) or column_index + 1 >= len(errmsg_words):
        raise err
    try:
        line = int(errmsg_words[line_index+1])
        column = int(errmsg_words[column_index+1])
        return _pretty_print_relevant_lines(contents, line - 1, column - 1) + errmsg
    except ValueError:
        # if the tokens we found weren't numbers
        raise err

def lint_contents(contents):
    """ Ensure that the string `contents` is a properly-formatted JSON file.
    raises ValueError if linting fails.
    """
    try:
        return json.loads(contents)
    except ValueError as err:
        msg = _describe_json_decode_error(contents, err)
        raise ValueError(msg)

def validate(filename):
    """ Ensure that the file located at `filename` contains a properly-formatted
    JSON file.
    raises ValueError if linting fails.
    """
    contents = ""
    with open(filename) as f:
        contents = f.read()
    return validate_contents(contents)

def validate_contents(contents):
    """ Ensure that the file located at `filename` contains a properly-formatted
    policy list. raises ValueError if linting fails, and ConfigError if a policy
    field is wrong.
    """
    conf = policy.Config()
    conf.load_from_dict(lint_contents(contents))
    return conf

def update(remote_url=constants.POLICY_REMOTE_URL, filename=constants.POLICY_LOCAL_FILE,
           force_update=False):
    """ Fetches and updates local copy of the policy file with the remote file,
    if local copy is outdated. """
    data = _get_remote_data(remote_url)
    remote_config = validate_contents(data)
    should_replace = True
    if os.path.isfile(filename):
        local_config = policy.Config(filename)
        local_config.load()
        should_replace = _should_replace(local_config, remote_config)
    if force_update or should_replace:
        with open(filename, 'w+') as handle:
            handle.write(data)
