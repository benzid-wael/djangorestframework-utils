# -*- coding: utf-8 -*-

from rest_framework import serializers


__all__ = ['modelserializer_factory']


def modelserializer_factory(model, serializer=None, fields=None, exclude=None):
    """
    Returns a ModelSerializer containing fields for the given model.

    :param model: model class.
    :param fields: is an optional list of field names. If provided, only the named
    fields will be included in the returned fields. If omitted or '__all__', all
    fields will be used.
    :param exclude: is an optional list of field names. If provided, the named fields
    will be excluded from the returned fields, even if they are listed in the ``fields``
    argument.
    :return: ModelSerializer class
    """

    # default values
    serializer = serializer or serializers.ModelSerializer

    attrs = {'model': model}
    if fields == '__all__':
        opts = model._meta.concrete_model._meta
        attrs['fields'] = [field.name for field in opts.fields if field.serialize]
    elif fields is not None:
        attrs['fields'] = fields
    if exclude is not None:
        attrs['exclude'] = exclude

    # create meta class
    parent = (object,)
    Meta = type('Meta', parent, attrs)

    # Give this new serializer class a reasonable name.
    class_name = model.__name__ + 'Serializer'

    # Class attributes for the new serializer class.
    serializer_class_attrs = {
        'Meta': Meta,
    }
    return type(serializer)(class_name, (serializer,), serializer_class_attrs)
