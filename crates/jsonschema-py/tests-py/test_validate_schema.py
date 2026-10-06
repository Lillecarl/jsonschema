import pytest

import jsonschema_rs

# An RE2 Unicode class, as Kubernetes CRDs write it. ECMA 262 has no `\PC`,
# so the meta-schema's `format: regex` rejects it.
SCHEMA = {"type": "string", "pattern": r"^\PC*$"}


def test_meta_schema_validation_is_on_by_default():
    with pytest.raises(jsonschema_rs.ValidationError):
        jsonschema_rs.validator_for(SCHEMA)


@pytest.mark.parametrize(
    "build",
    [
        lambda: jsonschema_rs.validator_for(SCHEMA, validate_schema=False),
        lambda: jsonschema_rs.Draft4Validator(SCHEMA, validate_schema=False),
        lambda: jsonschema_rs.Draft202012Validator(SCHEMA, validate_schema=False),
    ],
)
def test_validate_schema_false_builds_and_validates(build):
    validator = build()
    assert validator.is_valid("plain text")
    assert not validator.is_valid("bell \x07")


def test_validate_schema_false_on_the_one_shot_functions():
    assert jsonschema_rs.is_valid(SCHEMA, "x", validate_schema=False)
    assert not jsonschema_rs.is_valid(SCHEMA, "\x07", validate_schema=False)
