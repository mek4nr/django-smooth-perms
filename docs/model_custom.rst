Customization model
===================

We take the last example above::

  from django.db import models
  from smooth_perms.models import GlobalPermissionMixin, ModelPermission
  from smooth_perms.managers import GlobalPermissionManager

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
--------------------

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


If you want create your own validation, you can create your own function like bellow::

  def has_asucre_permission(self, request):
      ...
      return Boolean


.. note:: This function must be defined in ModelPermission (in our example it's ``MyModel``)

One for rules them all
----------------------

You can set ``smooth_perm_change_all`` to  change the basic change permission behaviour :

* Set to ``False`` (default), an user need to have the django change permission on Model, and can_change permission in Object for modifying this Object
* Set to ``True`` user only need the basic change permission for change all Objects on this model.

``smooth_perm_delete_all`` also exist for delete permission.

Low or High perm level
----------------------

For each model you can defined if permission are low or high. But in begin what is low & high :

* Low level : An user has permission if he has at least one time the permission in group or personal
* High level : An user has permission if **ALL** group and personal permission give this permission

For illustrate with an example, we take an user U1 and 2 groups G1 & G2, we base example on permission can_delete :

* Low level : if G1, G2 or U1 **has** permission **can_delete**, he **can** delete.
* High level : if G1, G2 or U1 **hasn't** permission **can_delete**, he **can't** delete.

By default we are in **low level** permission for simplify user experience. For change set the variable
``smooth_level_perm`` to ``SmoothPermAdmin.HIGH_LEVEL`` in your ``GlobalPermissionMixin``
