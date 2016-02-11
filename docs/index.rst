Django smooth perms documentation
=================================

**Django smooth perms - Smooth permission for Django admin**.

About
-----

Django smooth perms is an extension for `Django <http://www.djangoproject.com>`_ smooth permission in admin app (for object you want to).

Licence
-------

* Django smooth perms is licensed under `Creative Commons Attribution-NonCommercial 4.0 <http://creativecommons.org/licenses/by-nc/4.0/>`_ license.
* See licence and pricing: `In coming <#>`_

Requirements
------------

* Django 1.8.8
* Python 2.7.9

Installation
============

Install with github
-------------------

1. Go to your projects roots

2. Clone the project::
    git clone https://github.com/mek4nr/smooth_perms.git

Install with pip
----------------
1. Go to your projects roots

2. pip install django-smooth-perms


Settings.py
-----------

1. Add the ``'smooth-perms'`` application to the ``INSTALLED_APPS`` setting of your Django project ``settings.py`` file.::

    INSTALLED_APPS = (
        ...
        'smooth_perms',
        ...
    )


2. Add ``smooth_perms.middleware.user.CurrentUserMiddleware`` to the ``MIDDLEWARE_CLASSES``::

    MIDDLEWARE_CLASSES = (
        ...
        'smooth_perms.middleware.user.CurrentUserMiddleware',
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

How to add permissions to a model.

.. toctree::
   :maxdepth: 3

   model

Admin
-----

How to add permissions in admin

.. toctree::
   :maxdepth: 3

   admin

Smooth Registry Model
---------------------

How to custom behaviour for your permission

.. toctree::
   :maxdepth: 3

   registry
