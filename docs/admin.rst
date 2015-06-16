Admin
=====

Now we have our permissions in model, we need to configure admin
We gonna take a basic ``ModelAdmin`` like bellow::

    from .models import MyObject

    class MyObjectAdmin(admin.ModelAdmin):
        pass

    admin.site.register(MyModel, MyObjectAdmin)

Add inline permission in your ModelAdmin
----------------------------------------

So now we will add all stuff for see and manage permission in admin::

    from smooth_perms.admin import SmoothPermAdmin, SmoothPermInlineTabularAdmin
    from .models import MyObject, MyObjectPermission



    class MyObjectPermissionInline(SmoothPermInlineTabularAdmin):
        model = MyObjectPermission

    class MyObjectAdmin(SmoothPermAdmin):
        inline_perm_model = FormFactoryPermissionInline

        smooth_perm_field = {
        }

        fields = [...]

    admin.site.register(MyModel, MyObjectAdmin)


We create an Inline for the ModelPermission, who inheritance of ``SmoothPermInlineTabularAdmin``

We set the ``inline_perm_model`` to the name of your class just defined above.

So now we have define inline for permission and modelAdmin. (PS: you can add Inlines in your modeladmin)
The variable ``smooth_perm_field`` let you defined all field or inline show for every permission. For more info see `Define permission field`_

For each object you need to register in ``smooth_perm`` (you can do it in models.py if you want)


Define permission field
-----------------------

For each permission you can define witch field is readable, changeable or no visible.
You need to defined ``smooth_perm_field`` in your ``SmoothPermAdmin`` with syntax (we stay on can_%s permission)::

    smooth_perm_field =
    {
        '%s':
        {
            SmoothPermAdmin.INLINE : [ inline1, inline2 ]
            SmoothPermAdmin.FIELD : [ ['fieldexclude',True], 'fieldreadonly', ['fieldreadonly2', False]]
        }
    }

For each permission ``%s`` you define set ``INLINE`` you show (or hide if user doesn't have permission),
For ``FIELD`` is a list of field you want to set changeable or readonly. If you want exclude a field
if user doesn't have permission, replace the name of field by a couple ['field',True] where True mean
field is exclude. If you just list the field by default it's readonly.

.. note:: Like example you can mix itd

