""" Main entrypoint for starttls-policy CLI tool """
import argparse
import os
import sys

from starttls_policy import configure
from starttls_policy import constants
from starttls_policy import lint

GENERATORS = {
    "postfix": configure.PostfixGenerator,
}

def _argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lint", help="Lint the policy file.", action="store_true",
                        default=False, required=False)
    parser.add_argument("--generate", help="The MTA you want to generate a configuration file for.",
                        dest="generate", required="--lint" not in sys.argv)
    # TODO: decide whether to use /etc/ for policy list home
    parser.add_argument("--policy-dir", help="Policy file directory on this computer.",
                        default="/etc/starttls-policy/", dest="policy_dir")
    return parser


def _ensure_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def _lint(arguments):
    lint.validate(os.path.join(arguments.policy_dir, constants.POLICY_FILENAME))

def _generate(arguments):
    _ensure_directory(arguments.policy_dir)
    config_generator = GENERATORS[arguments.generate](arguments.policy_dir)
    config_generator.generate()
    config_generator.manual_instructions()

def _perform(arguments, parser):
    if arguments.lint:
        _lint(arguments)
        return
    if arguments.generate not in GENERATORS:
        parser.error("no configuration generator exists for '%s'" % arguments.generate)
    _generate(arguments)

def main():
    """ Entrypoint for CLI tool. """
    parser = _argument_parser()
    _perform(parser.parse_args(), parser)

if __name__ == "__main__":
    main()  # pragma: no cover
