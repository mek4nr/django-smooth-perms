Presentation
============

Description
-----------

Smooth perms in a module for django admin. He allow you to defined smooth perms for your admin object.
He is easy to set up and override.

Smooth perms is divide on 2 different perms system :

* The basic permission provide by Django : **can_add, can_change, can_delete** (this 3 permissions have the basic behaviour).
* The model permission provide by smooth perms.


What Smooth perms allow you :

* You can defined, for each object any permission you want for each group or user.
* For each object created, the user who created him, is called the ``owner`` and have all permissions on this object.
* An user can't give a permission, he doesn't have.
* Defined what field for each perm
* Custom permissions
* High or Low permissions (see `Model Customization <model_custom.html#low-or-high-perm-level>`_ for further information)

Basic permissions
-----------------

Smooth perms provide this basics permissions :

* **can_change** : User can change this object
* **can_advanced_settings** : User can change advanced setting in object (define by dev)
* **can_delete** : User can delete this object
* **can_change_permissions** : User can add or change permissions in object
* **can_delete_permissions** : User can delete permissions
* **can_view** : User can only see field in read_only

For each permission you can defined witch field is readable, changeable or exclude.
See `Admin <admin.html>`_ configuration for more information.

Custom permissions
------------------

You can defined your own permission, and theirs behaviours.
See `Model <model_custom.html>`_ for the definition and behaviours.

