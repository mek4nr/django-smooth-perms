Django smooth perms documentation
=================================

**Django smooth perms - Smooth permission for Django admin**.

About
-----

Django smooth perms is an extension for `Django <http://www.djangoproject.com>`_ smooth permission in admin app (for object you want to).
This extension is currently in development.

Licence
-------

* Django smooth perms is licensed under `Creative Commons Attribution-NonCommercial 4.0 <http://creativecommons.org/licenses/by-nc/4.0/>`_ license.
* See licence and pricing: `In coming <#>`_


Installation
============

1. You can get Django Suit by using pip or easy_install::

    pip install django-smooth-perms


2. You will need to add the ``'smooth-perms'`` application to the ``INSTALLED_APPS`` setting of your Django project ``settings.py`` file.::

    INSTALLED_APPS = (
        ...
        'smooth_perms',
        ...
    )




Presentation
============

.. toctree::
   :maxdepth: 3

   description


Customization
=============

Models
------

How add permissions to a model.

.. toctree::
   :maxdepth: 3

   model

Customization for model
-----------------------

How custom your permission.

.. toctree::
   :maxdepth: 3

   model_custom

Admin
-----

How add permissions in admin

.. toctree::
   :maxdepth: 3

   admin

Group's Permission
------------------

Create an custom and user-friendly group design

.. toctree::
   :maxdepth: 3

   group