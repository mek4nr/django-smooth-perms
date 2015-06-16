Friendly auth design
====================

Smooth perms provide you a friendly user auth design. Let's see how configure it

Configuration
-------------

In begin you need to register each object you want in, with smooth_registry::

    from smooth_perms.admin import smooth_registry

    smooth_registry.register(MyModel, 'text')

.. note:: The second param is set to the verbose name of model by default.

After you need to create a ModelAdmin and ModelForm for ``Group`` using inheritance provide by smooth perms::

    from smooth_perms.admin import SmoothGroupAdmin, SmoothGroupForm, SmoothGroup

    class MyGroupForm(SmoothGroupForm):
        pass

    class MyGroup(SmoothGroupAdmin):
        form = MyGroupForm

    admin.site.register(SmoothGroup, MyGroup)

And for finish, you need to add for each model registry ::

    can_add_%s = forms.BooleanField(label=_('Add'), required=False)
    can_change_%s = forms.BooleanField(label=_('Change'), required=False)
    can_delete_%s = forms.BooleanField(label=_('Delete'), required=False)


.. note:: Here %s is the name of the database, for our example for MyObject is ``can_add_myobject``.

.. note:: SmoothGroup and User are natively in smooth_registry.
