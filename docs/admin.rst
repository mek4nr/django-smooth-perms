Admin
=====

Now we have our permissions in model, we need to configure admin
We gonna take a basic ``ModelAdmin`` like below::

    from .models import MyObject

    @admin.register(MyObject)
    class MyObjectAdmin(admin.ModelAdmin):
        pass


Add inlines permissions in your ModelAdmin
------------------------------------------

So now we will add all stuff to see and manage permission in admin::

    from smooth_perms.admin import SmoothPermAdmin, SmoothPermInlineTabularAdmin
    from smooth_perms.utils.registry import smooth_registry
    from .models import MyObject, MyObjectPermission


    class MyObjectPermissionInline(SmoothPermInlineTabularAdmin):
        model = MyObjectPermission


    @admin.register(MyObject)
    class MyObjectAdmin(SmoothPermAdmin):
        inline_perm_model = MyObjectPermissionInline


We create an Inline for the ModelPermission, who inheritance of ``SmoothPermInlineTabularAdmin``

We set the ``inline_perm_model`` to the name of your class just defined above.

So now we have define inline for permission and modelAdmin. (PS: you can add Inlines in your modeladmin)
The variable ``smooth_perm_field`` let you defined all field or inline show for every permission. For more info see `Define permission field <registry.html#modify-fields-permissions>`_

For each object you need to register in ``smooth_perm`` (you can do it in models.py if you want)

Admin with multiples inlines
----------------------------

If your model need inlines in your admin, you just have to do as always using smooth_perms
``ModelAdmin`` provide:

* In **models.py**::

    class MyModel(ModelPermission):
     ...

    class MyInlineObject(models.Model)
        fk = models.ForeignKey(MyModel)


* In **admin.py**::


    from smooth_perms.admin import SmoothPermAdmin, SmoothPermInlineTabularAdmin
    from smooth_perms.utils.registry import smooth_registry
    from .models import MyObject, MyObjectPermission, MyInlineObject

    class InlineForMyobject(SmoothPermTabularInline):
        model = AccessRPC


    class MyObjectPermissionInline(SmoothPermInlineTabularAdmin):
        model = MyObjectPermission


    @admin.register(MyObject)
    class MyObjectAdmin(SmoothPermAdmin):
        inline_perm_model = MyObjectPermissionInline


Now you can set the permission with MyObjectPermissionInline in your admin. And now you
need to defined behaviour for all your fields with all your permissions.
See `Registry <registry.html>`_
