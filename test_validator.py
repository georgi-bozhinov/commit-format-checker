import pytest
from validator import validate


VALID_MESSAGES =  [
    "feature(app.py): Add changes to the file",
    "docs(app_2.js): Remove documentation",
    """fix(app.py): Fixed issue #250 \n\nBREAKING CHANGES: Changed x method""",
    """fix(app.py): Fixed issue #250\nProvided a fix for the issue that fixes it. \n\nBREAKING CHANGES: Changed x method""",
    "feature: add changes to file",
]
INVALID_MESSAGES =  [
    "Add change to app.py",
    "fix(app.py): Fixed issue #250 BREAKING CHANGES: Changed x method",
]


@pytest.mark.parametrize("msg", VALID_MESSAGES)
def test_validation_on_valid_messages(msg):
    """ Test valid commit message validation """
    assert validate(msg) == True


@pytest.mark.parametrize("msg", INVALID_MESSAGES)
def test_validation_on_invalid_messages(msg):
    """ Test invalid commit message validation """
    assert validate(msg) == False
