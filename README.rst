django-rest-utils
=================

|build-status-image| |pypi-version|

Overview
--------

Utilities for Django REST Framework

Requirements
------------

-  Python (2.7, 3.3, 3.4)
-  Django (1.6, 1.7, 1.8)
-  Django REST Framework (3.0, 3.1)

Installation
------------

Install using ``pip``\ …

.. code:: bash

    $ pip install django-rest-utils

Features
--------

* VerboseMetadata (which is more verbose and not ambiguous like ``SimpleMetadata``)
* modelserializer_factory


VerboseMetadata features
------------------------

* Add field's ``allow_null`` and ``default`` properties
* Include ``pattern`` property for ``RegexField``
* Include ``max_digits`` and ``decimal_places`` properties for ``DecimalField``

For further information, see the [documentation](http://benzid_wael.github.io/django-rest-utils/docs).

Example
-------

TODO: Write example.


Documentation & Support
-----------------------

Full documentation for the project is available at `docs`_.

You may also want to follow the `author`_ on Twitter.


.. _tox: http://tox.readthedocs.org/en/latest/
.. _author: https://twitter.com/benzid_wael

.. |build-status-image| image:: https://secure.travis-ci.org/benzid-wael/django-rest-utils.svg?branch=master
   :target: http://travis-ci.org/benzid-wael/django-rest-utils?branch=master
.. |pypi-version| image:: https://img.shields.io/pypi/v/django-rest-utils.svg
   :target: https://pypi.python.org/pypi/django-rest-utils
