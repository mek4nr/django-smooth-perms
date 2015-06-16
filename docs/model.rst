Models Permissions
==================

Smooth permission allow you, to create permission on each model easily.


Model example
-------------

For this part, we have this model::

  from django.db import models

  class MyModel(models.Model):
     ...



Add permissions to this model
-----------------------------

For create and associate model to model permission, you need to create 2 classes, and update inheritance of model like bellow::

  from django.db import models
  from smooth_perms.models import GlobalPermissionMixin, ModelPermission
  from smooth_perms.managers import GlobalPermissionManager

  class MyModelPermissionManager(GlobalPermissionManager):
    foreign_key = 'fk_object'

  class MyModelPermission(GlobalPermissionMixin):
     fk_object = models.ForeignKey('MyModel')

     objects = MyModelPermissionManager()

  class MyModel(ModelPermission):
     ...
     permissions = MyModelPermission


.. important:: The content of ``foreign_key`` in ``GlobalPermissionManager`` must be the variable name of model foreign key in ``GlobalPermissionMixin``

.. important:: The class ``GlobalPermissionMixin`` must be defined before ``ModelPermission``

.. note:: The attribute ``permission`` just need a model class not an instance.
Now we can add permission for each instance of MyModel


Create a custom permission
--------------------------

Smooth perms allow you to create custom permission for each model.
For this you need to do 2 things :

* Create your permissions with this syntax : ``can_%s = models.BooleanField()``
* Create or update ``PERMISSIONS`` variable in your ``GlobalPermissionMixin`` (you don't need this variable if you use basic permissions), she must contain the name ( the ``%s`` in ``can_%s``)
::

  class MyModelPermission(GlobalPermissionMixin):
     fk_object = models.ForeignKey('MyModel')

     PERMISSIONS = ('asucre',)

     can_asucre = models.BooleanField(_("can a sucre"), default=False)

     objects = MyModelPermissionManager()


