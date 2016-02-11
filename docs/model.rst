Configuration of Models
=======================

Add permission to an existing model.

Model example
-------------

We will take this model for example on all documentation::

  from django.db import models

  class MyModel(models.Model):
     ...



Add permissions to this model
-----------------------------

To add permission system to ``MyModel``, you need to :
* Add a manager using ``GlobalPermissionManager``
* A model permission using ``GlobalPermissionMixin``
* And your model need to be a ``ModelPermission`` model.

Like sample below::

  from django.db import models
  from smooth_perms.models import GlobalPermissionMixin, ModelPermission, GlobalPermissionManager

  class MyModelPermissionManager(GlobalPermissionManager):
    foreign_key = 'fk_object'

  class MyModelPermission(GlobalPermissionMixin):
     fk_object = models.ForeignKey('MyModel')

     objects = MyModelPermissionManager()

  class MyModel(ModelPermission):
     ...
     permissions = MyModelPermission


.. important:: The content of ``foreign_key`` in ``GlobalPermissionManager`` must be the field name of model foreign-key's in ``GlobalPermissionMixin``

.. important:: The class ``GlobalPermissionMixin`` must be defined before ``ModelPermission``

.. note:: The attribute ``permissions`` need to be a model class not an instance.

The model are now setup, it rest just to setup admin, see `Admin <admin.html>`_

Basic permission
----------------

Now you have model with basic permissions:

* **view** - Needed to see the object in read_only
* **change** - Needed to change the object
* **advanced_settings** - You need to customize the effect
* **delete** - Needed to delete the object
* **change_permissions** - Needed to add/remove permissions for the object
* **delete_permissions** - Needed to delete permissions for the object

But you can create your own permission. See below

Create a custom permission
--------------------------

For create your own permission you need to modify your ``GlobalPermissionMixin`` model like this :

* Create your permissions (model field) with this syntax : ``can_%s = models.BooleanField()``
* Create or update ``PERMISSIONS`` variable in your ``GlobalPermissionMixin`` (you don't need this variable if you use basic permissions), she must contain the name ( the ``%s`` in ``can_%s``)

In our exemple we will add the permission ``can_asucre``::

  class MyModelPermission(GlobalPermissionMixin):
     fk_object = models.ForeignKey('MyModel')

     PERMISSIONS = ('asucre',)

     can_asucre = models.BooleanField(_("can a sucre"), default=False)

     objects = MyModelPermissionManager()



.. warning:: Don't forget to migrate and reload server

Customization model
-------------------

We take the last example above::

  from django.db import models
  from smooth_perms.models import GlobalPermissionMixin, ModelPermission, GlobalPermissionManager

  class MyModelPermissionManager(GlobalPermissionManager):
    foreign_key = 'fk_object'

  class MyModelPermission(GlobalPermissionMixin):
     fk_object = models.ForeignKey('MyModel')

     PERMISSIONS = ('asucre',)

     can_asucre = models.BooleanField(_("can a sucre"), default=False)

     objects = MyModelPermissionManager()

  class MyModel(ModelPermission):
     ...
     permissions = MyModelPermission


Permission functions
^^^^^^^^^^^^^^^^^^^^

For each permission you can defined a function ``has_%s_permission(self, request)`` in ModelPermission.
If you don't create this function for your new permission, the generic function is called::

    def has_generic_permission(self, request, permission_type):

      user = request.user
      if not user.is_authenticated():
          return False
      elif user.is_superuser:
          return True
      elif user == self.owner:
          return True
      else:
          permission = self.permissions.objects.get_smooth_id_list(user, permission_type)
          if permission == GlobalPermissionManager.get_grant_all():
              return True
          else:
              return self.id in permission


You can override the behavior of all permission by update the function like this::

    def has_%s_permission(self, request):
        ...
        return Boolean

If we take last exemple we will override the ``has_asucre_permission``::

  def has_asucre_permission(self, request):
      return True


.. note:: This function must be defined in ModelPermission (in our example it's ``MyModel``)

One for rules them all
^^^^^^^^^^^^^^^^^^^^^^

You can set ``smooth_perm_change_all`` to  change the basic change permission behaviour :

* Set to ``False`` (default), a user need to have the django change permission on Model, and can_change permission in Object to modifying this Object
* Set to ``True`` user only need the basic change permission to change all Objects on this model.

``smooth_perm_delete_all`` also exist to delete permission.

Low or High perm level
^^^^^^^^^^^^^^^^^^^^^^

For each model you can defined if permission are low or high:

* Low level : a user has permission if he has at least one time the permission in group or personal
* High level : a user has permission if **ALL** group and personal permission give this permission

To illustrate with an example, we take a user U1 and 2 groups G1 & G2, we base example on permission can_delete :

* Low level : if G1, G2 or U1 **has** permission **can_delete**, he **can** delete.
* High level : if G1, G2 or U1 **hasn't** permission **can_delete**, he **can't** delete.

By default we are in **low level** permission to simplify user experience. To change set the variable
``smooth_level_perm`` to ``SmoothPermAdmin.HIGH_LEVEL`` in your ``GlobalPermissionMixin``
