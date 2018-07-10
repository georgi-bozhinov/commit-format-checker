"""
Module to validate if a git commit message is in a valid predefined format and return an error if it's not
Functions as a git commit-msg hook
"""

import re
import sys

BREAKING_CHANGES = 'BREAKING CHANGES'
ERROR_MESSAGE = \
"""
Commit must be in the form:
<feature|fix|style|docs|test>(<file>): <description>

<detailed description> ( optional )

<BREAKING CHANGES>: <description> ( optional )
"""

BASE_FORMAT = r'(feature|fix|style|docs|text)(\([a-zA-Z0-9._-]*\)): *\w+'
CHANGE_FORMAT = r'({}): *.*'.format(BREAKING_CHANGES)

def _validate_first_line(msg):
    """
    Validates that the first line
    ( could also be only line if there is no breaking change )
    of a commit message is valid
    """
    if BREAKING_CHANGES in msg:
        return False

    if re.match(BASE_FORMAT, msg):
        return True

    return False


def _validate_description(msg):
    """
    Validates that the description is a string
    and does not include the breaking changes word
    """
    if BREAKING_CHANGES in msg:
        return False

    if re.match(r'.*', msg):
        return True

    return False


def _validate_breaking_change_line(msg):
    """
    Validates that a line containing a breaking change message
    is of valid format
    """
    if re.match(CHANGE_FORMAT, msg):
        return True

    return False


VALIDATORS = [
    _validate_first_line,
    _validate_description
]


def validate(msg):
    """
    Validates a git commit message to be in the following format:
    <feature|fix|style|docs|test>(<file(s)>): <description>

    <detailed description>

    <BREAKING CHANGES>: <description>

    For example:
    docs(validator.py): Add docstring to validate function

    BREAKING CHANGES: Deleted the function
    """
    messages = re.split(r'\n+', msg)
    is_valid = True
    for idx, message in enumerate(messages):
        if not message.startswith(BREAKING_CHANGES):
            is_valid = is_valid and VALIDATORS[idx](message)
        else:
            is_valid = is_valid and _validate_breaking_change_line(message)

    return is_valid


def main():
    commit = sys.argv[1]
    with open(commit, 'r') as f:
        msg = f.read()

    if not validate(msg):
        print(ERROR_MESSAGE)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
