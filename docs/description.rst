Presentation
============

Description
-----------

Smooth perms is a module for django admin. He allow you to define smooth perms for your admin objects.
He is easy to set up and/or override.

Smooth perms use 2 different permissions systems :

* The basic permissions provided by Django : **can_add, can_change, can_delete** (this 3 permissions have the basic behaviour).
* The model permissions provided by smooth perms.


What Smooth perms allow you :

* You can add smooth perm on all your models
* You can define, for each model your customs permissions
* You define, for each model and permissions, the behaviour (fields shown or not), directly in admin view
* System of owner, who grant all permissions to creator of one object
* An user can't give a permission he doesn't have.
* High or Low level of permissions (see `Model Customization <model.html#low-or-high-perm-level>`_ for further information)
* An user friendly group model for custom add, change, delete permissions

Permissions
-----------

Basic permissions
^^^^^^^^^^^^^^^^^

Smooth perms provide this basics permissions :

* **view** - Needed to see the object in read_only
* **change** - Needed to change the object
* **advanced_settings** - You need to customize the effect
* **delete** - Needed to delete the object
* **change_permissions** - Needed to add/remove permissions for the object
* **delete_permissions** - Needed to delete permissions for the object

For each permission you can defined witch field is readable, changeable or exclude.
See `Field registry <registry.html#modify-fields-permissions>`_ configuration for more information.

Custom permissions
^^^^^^^^^^^^^^^^^^

You can defined your own permission, and theirs behaviours.
See `Model <model.html>`_ for the definition and behaviours.

Admin
-----

Smooth Registry
^^^^^^^^^^^^^^^

You can define behaviours for all permissions, in admin, thanks to Smooth registry model.
See `Registry <registry.html>`_ for more information.

Smooth Group
^^^^^^^^^^^^

A group model is define with a friendly user admin, for add django native permission to a group (add, change, delete).
He is configure to have all model register in ``smooth_registry``. See `Registry <registry.html>`_ for more information.
.. note:: SmoothGroup and User are natively in smooth_registry.