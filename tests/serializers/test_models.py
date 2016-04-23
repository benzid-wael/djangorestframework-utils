# -*- coding: utf-8 -*-
import sys
import pytest

from django.db import models
from django.core.exceptions import ImproperlyConfigured

from rest_framework import serializers

from drf_utils.metadata import VerboseMetadata
from drf_utils.serializers.models import modelserializer_factory


class Person(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField(null=True)


class InvalidPersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ['nonexistant']


class TestModelSerializerFactory(object):

    @classmethod
    def setup_class(cls):
        cls.minimal_data = {
            'name': 'John Doe'
        }
        cls.person_data = {
            'name': "Ali Baba",
            'age': 126
        }

    def test_serializer_name(self):
        serializer = modelserializer_factory(Person)(data=self.minimal_data)
        assert serializer.__class__.__name__ == 'PersonSerializer'

    def test_with_minimal_argument(self):
        # 1st case
        serializer = modelserializer_factory(Person)(data=self.minimal_data)
        assert serializer.is_valid() is True
        assert serializer.data == dict(name="John Doe")
        # 2nd case
        serializer = modelserializer_factory(Person)(data=self.person_data)
        assert serializer.is_valid() is True
        assert serializer.data == dict(name="Ali Baba", age=126)

    def test_no_fields(self):
        serializer = modelserializer_factory(Person, fields=())(data=self.person_data)
        assert serializer.is_valid() is True
        assert serializer.data == dict()

    def test_including_all_fields(self):
        serializer = modelserializer_factory(Person, fields="__all__")(data=self.person_data)
        assert serializer.is_valid() is True
        assert serializer.data == dict(name="Ali Baba", age=126)

    def test_extra_field_modelform_factory(self):
        serializer = modelserializer_factory(
            Person,
            fields=['name']
        )(data={"name": "joe", "age": 34})
        serializer.is_valid()
        assert serializer.data == dict({"name": "joe"})

    def test_limit_non_existant_field(self):
        # 1st case: created by inheritance
        with pytest.raises(ImproperlyConfigured):
            serializer = InvalidPersonSerializer(data={"name": "joe"})
            serializer.is_valid()
        # 2nd case: created by .modelserializer_factory()
        with pytest.raises(ImproperlyConfigured):
            serializer = modelserializer_factory(Person, fields=['nonexistant'])(data={"name": "joe"})
            serializer.is_valid()

    def test_exclude_fields(self):
        serializer = modelserializer_factory(Person, exclude=['age'])(data=self.person_data)
        assert serializer.is_valid() is True
        assert serializer.data == dict(name="Ali Baba")

    def test_excluding_fields(self):
        serializer = modelserializer_factory(Person, exclude=['name'])(data=self.person_data)
        assert serializer.is_valid() is True
        assert serializer.data == dict(age=126)

    @pytest.mark.xfail(sys.version_info >= (3, 0),
                       reason="In Python3, dict.keys() returns an iterable")
    def test_metadata(self):
        metadata = VerboseMetadata()
        serializer = modelserializer_factory(Person)(data=self.person_data)
        serializer_info = metadata.get_serializer_info(serializer)
        assert serializer_info.keys() == ['id', 'name', 'age']

    @pytest.mark.skipif(sys.version_info < (3, 0),
                        reason="Test only for Python 3")
    def test_metadata_py3(self):
        metadata = VerboseMetadata()
        serializer = modelserializer_factory(Person)(data=self.person_data)
        serializer_info = metadata.get_serializer_info(serializer)
        assert list(serializer_info.keys()) == ['id', 'name', 'age']
