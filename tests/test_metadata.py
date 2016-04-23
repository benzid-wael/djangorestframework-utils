# -*- coding: utf-8 -*-
import pytest

from rest_framework import serializers

from django_rest_utils.metadata import VerboseMetadata


def compareDict(dict1, dict2):
    match = True
    for key in dict1:
        if key not in dict2 or dict1[key] != dict2[key]:
            match = False
            break
    return match


@pytest.mark.parametrize(("field", "expected"), [
    (serializers.Field(), {
        'type': 'field',
        'allow_null': False,
        'read_only': False,
        'required': True,
    }),
    (serializers.Field(label="Some field"), {
        'label': "Some field",
        'type': 'field',
        'allow_null': False,
        'read_only': False,
        'required': True,
    }),
    (serializers.ReadOnlyField(), {
        'type': 'field',
        'allow_null': False,
        'read_only': True,
        'required': False,
    }),
    (serializers.Field(allow_null=True), {
        'type': 'field',
        'allow_null': True,
        'read_only': False,
        'required': True,
    }),
    (serializers.Field(default=23), {
        'type': 'field',
        'allow_null': False,
        'read_only': False,
        'required': False,
        'default': 23
    }),
    (serializers.Field(default=20, allow_null=True), {
        'type': 'field',
        'allow_null': True,
        'read_only': False,
        'required': False,
        'default': 20
    }),
    (serializers.BooleanField(), {
        'type': 'boolean',
        'allow_null': False,
        'read_only': False,
        'required': True,
    }),
    (serializers.BooleanField(default=True), {
        'type': 'boolean',
        'allow_null': False,
        'read_only': False,
        'required': False,
        'default': True
    }),
    (serializers.NullBooleanField(), {
        'type': 'boolean',
        'allow_null': True,
        'read_only': False,
        'required': True,
    }),
    (serializers.NullBooleanField(default=None), {
        'type': 'boolean',
        'allow_null': True,
        'read_only': False,
        'required': False,
        'default': None
    }),
    (serializers.DecimalField(max_digits=10, decimal_places=2), {
        'type': 'decimal',
        'allow_null': False,
        'read_only': False,
        'required': True,
        'max_digits': 10,
        'decimal_places': 2

    }),
    (serializers.FloatField(), {
        'type': 'float',
        'allow_null': False,
        'read_only': False,
        'required': True,

    }),
])
def test_field_repr(field, expected):
    meta = VerboseMetadata()
    res = meta.get_field_info(field)
    assert compareDict(res, expected) is True
