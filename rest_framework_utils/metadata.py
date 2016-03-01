# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import collections

from django.utils.encoding import force_text
from django.core.validators import RegexValidator

from rest_framework import metadata
from rest_framework import serializers
from rest_framework.utils.field_mapping import ClassLookupDict
from rest_framework.fields import empty


class VerboseMetadata(metadata.SimpleMetadata):
    """
    This is an enhanced metadata implementation.
    It returns an ad-hoc set of information about the view.

    Compared to default REST metadata class, this class will remove any confuse about the view, For example,
    ``SimpleMetadata`` represents both BooleanField and NullBooleanField in the same form, etc.
    """
    label_lookup = ClassLookupDict({
        serializers.Field: 'field',
        serializers.BooleanField: 'boolean',
        serializers.NullBooleanField: 'boolean',
        serializers.CharField: 'string',
        serializers.URLField: 'url',
        serializers.EmailField: 'email',
        serializers.RegexField: 'regex',
        serializers.SlugField: 'slug',
        serializers.IntegerField: 'integer',
        serializers.FloatField: 'float',
        serializers.DecimalField: 'decimal',
        serializers.DateField: 'date',
        serializers.DateTimeField: 'datetime',
        serializers.TimeField: 'time',
        serializers.ChoiceField: 'choice',
        serializers.MultipleChoiceField: 'multiple choice',
        serializers.FileField: 'file upload',
        serializers.ImageField: 'image upload',
        serializers.ListField: 'list',
        serializers.DictField: 'nested object',
        serializers.Serializer: 'nested object',
    })

    def get_field_info(self, field):
        """
        Given an instance of a serializer field, return a dictionary
        of metadata about it.
        """
        field_info = collections.OrderedDict()
        field_info['type'] = self.label_lookup[field]
        field_info['required'] = getattr(field, 'required', False)

        attrs = [
            'read_only', 'label', 'help_text', 'allow_null',
            'min_length', 'max_length',
            'min_value', 'max_value',
        ]

        # Handle default attribute
        default_value = getattr(field, 'default')
        if (default_value is not empty):
            field_info['default'] = force_text(default_value, strings_only=True)

        for attr in attrs:
            value = getattr(field, attr, None)
            if value is not None and value != '':
                field_info[attr] = force_text(value, strings_only=True)

        if hasattr(field, 'choices'):
            field_info['choices'] = [
                {
                    'value': choice_value,
                    'display_name': force_text(choice_name, strings_only=True)
                }
                for choice_value, choice_name in field.choices.items()
            ]

        # handle RegexField
        if isinstance(field, serializers.RegexField):
            pattern = None
            for validator in field.validators:
                if isinstance(validator, RegexValidator):
                    pattern = validator.regex.pattern
                    break
            field_info['pattern'] = force_text(pattern, strings_only=True)

        # handle DecimalField
        if isinstance(field, serializers.DecimalField):
            for attr in ('max_digits', 'decimal_places'):
                field_info[attr] = force_text(getattr(field, attr), strings_only=True)

        return field_info