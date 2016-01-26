from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin, BaseModelAdmin
from django.contrib.admin.utils import flatten_fieldsets
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.contrib.auth import get_user_model
from copy import deepcopy, copy
from django.db.models.base import ModelBase
from django.core.exceptions import ImproperlyConfigured
from django.contrib.admin.sites import AlreadyRegistered, NotRegistered
from django.utils.translation import ugettext_lazy, ugettext as _
from django.forms.utils import ErrorList
from django import forms
from smooth_perms.managers import PermissionNotFoundException
from smooth_perms.models import SmoothGroup, SmoothUser


class SmoothPermRegister(object):
    registry = []

    def get_codename(self, model, perm):
        return getattr(model._meta, 'get_{}_permission' .format(perm))()

    def get_fields_form(self, fields=None):
        """
        Create automatically fields for group admin form
        Not Used because impossible to call __init__ on ModelForm
        :param fields:
        :return:
        """
        fields = fields or {}
        for model, text in self.registry:
            for t in ('add', 'change', 'delete'):
                # add permission `t` to model `model`
                fields['can_{}' . format(self.get_codename(model, t))] = forms.BooleanField(label=_(t.title()), required=False)
        return fields

    def get_initials(self, obj):
        """
        Read out permissions from permission system.
        """
        initials = {}
        permission_accessor = getattr(obj, 'permissions')

        for model, text in self.registry:
            name = model.__name__.lower()
            content_type = ContentType.objects.get_for_model(model)
            permissions = permission_accessor.filter(content_type=content_type).values_list('codename', flat=True)
            for t in ('add', 'change', 'delete'):
                codename = self.get_codename(model, t)
                initials['can_{}_{}'  .format(t, name)] = codename in permissions
        return initials

    def save_permissions(self, data, obj):

        if not obj.pk:
            # save obj, otherwise we can't assign permissions to him
            obj.save()
        permission_acessor = getattr(obj, 'permissions')
        for model, text in self.registry:
            content_type = ContentType.objects.get_for_model(model)
            for t in ('add', 'change', 'delete'):
                # add permission `t` to model `model`
                codename = self.get_codename(model, t)
                permission = Permission.objects.get(content_type=content_type, codename=codename)
                if data.get('can_{}' . format(codename), None):
                    permission_acessor.add(permission)
                else:
                    permission_acessor.remove(permission)

    def register(self, model, text=None):
        if not isinstance(model, ModelBase):
            raise ImproperlyConfigured('This object {} is not a ModelBase class' . format(model.__name__))

        for m, t in self.registry:
            if m == model:
                raise AlreadyRegistered('The model {} is already registered' . format(model.__name__))

        if text is None:
            text = u'{} permissions' .format(model.__name__)

        self.registry.append((model, _(text)))

    def unregister(self, model):
        for i, perm_model in enumerate(self.registry):
            m, t = perm_model
            if model == m:
                self.registry.remove(i)
                return True
        raise NotRegistered('The model {} is not registered' . format(model.__name__))

    def update_permission_fieldsets(self, request, fieldsets):
        """
        Nobody can grant more than he haves, so check for user permissions
        to Page and User model and render fieldsets depending on them.
        """
        fieldsets = deepcopy(fieldsets)

        for i, perm_model in enumerate(self.registry):
            model, title = perm_model
            opts, fields = model._meta, []
            name = model.__name__.lower()

            for t in ('add', 'change', 'delete'):
                if request.user.has_perm('{}.{}_{}' .format(opts.app_label, t, name)):
                    fields.append('can_{}_{}' . format(t, name))
            if fields:
                fieldsets.insert(2 + i, (title, {'fields': (fields,)}))
        return fieldsets

smooth_registry = SmoothPermRegister()
smooth_registry.register(SmoothUser)
smooth_registry.register(SmoothGroup)


class SmoothGroupForm(forms.ModelForm):
    """
    Generic form for User & Group permissions in cms
    """

    can_add_smoothgroup = forms.BooleanField(label=_('Add'), required=False)
    can_change_smoothgroup = forms.BooleanField(label=_('Change'), required=False)
    can_delete_smoothgroup = forms.BooleanField(label=_('Delete'), required=False)

    can_add_smoothuser = forms.BooleanField(label=_('Add'), required=False)
    can_change_smoothuser = forms.BooleanField(label=_('Change'), required=False)
    can_delete_smoothuser = forms.BooleanField(label=_('Delete'), required=False)

    class Meta:
        fields = ['name']
        model = SmoothGroup

    def __init__(self, data=None, files=None, auto_id='id_{}', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        if instance:
            initial = initial or {}
            initial.update(self.populate_initials(instance))

        super(SmoothGroupForm, self).__init__(data, files, auto_id, prefix,
                                              initial, error_class, label_suffix, empty_permitted, instance)

    def populate_initials(self, obj):
        return smooth_registry.get_initials(obj)

    def save(self, commit=True):
        group = super(SmoothGroupForm, self).save(commit=False)
        smooth_registry.save_permissions(self.cleaned_data, group)
        return group


class SmoothGroupAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ('name',)}),
    ]

    form = SmoothGroupForm

    def get_fieldsets(self, request, obj=None):
        return smooth_registry.update_permission_fieldsets(request, self.fieldsets)

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        if obj.pk is None:
            obj.owner = request.user
        obj.save()


class SmoothPermInlineTabularAdmin(admin.TabularInline):
    """
    Class form inline permission
    """

    extra = 0

    def has_change_permission(self, request, obj=None):
        """
        Standard change permission, if inline is show user can add & change
        """
        return True

    def has_add_permission(self, request):
        """
        Standard add permission, if inline is show user can add & change
        """
        return True

    def has_delete_permission(self, request, obj=None):
        """
        Standard delete permission, can_delete is init from get_formset
        """
        return self.can_delete

    def get_formset(self, request, obj=None, **kwargs):
        """
        Some fields may be excluded here. User can change only
        permissions which are available for him. E.g. if user does not haves
        can_publish flag, he can't change assign can_publish permissions.
        """
        exclude = self.exclude or []

        if obj is not None:
            for perm in getattr(getattr(obj, 'permissions')(), 'PERMISSIONS'):
                if not obj.has_generic_permission(request, perm):
                    exclude.append('can_{}' . format(perm))

            self.can_delete = obj.has_delete_permissions_permission(request)

        formset_cls = super(SmoothPermInlineTabularAdmin, self).get_formset(request, obj=None, exclude=exclude, **kwargs)
        return formset_cls


class SmoothPermBaseModelAdmin(BaseModelAdmin):
    pass


class SmoothPermAdmin(admin.ModelAdmin):
    """
    Class for model admin of object with permission, need at least one attr
    :param inline_perm_model: the model inline for permission
    :param smooth_perm_field: all field considered like advanced_settings on the model,
    they will be read_only if user has not permission
    """

    INLINE = 0
    FIELD = 1

    smooth_perm_field = {}

    exclude_from_parent = ()
    fieldsets_from_parent = []

    inline_perm_model = SmoothPermInlineTabularAdmin

    def __init__(self, *arg, **kwargs):
        if self.exclude is not None:
            self.exclude_from_parent = tuple(self.exclude)

        if self.fieldsets is not None:
            self.fieldsets_from_parent = list(self.fieldsets)

        super(SmoothPermAdmin, self).__init__(*arg, **kwargs)

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        if obj.pk is None:
            obj.owner = request.user
        obj.save()

    def has_change_permission(self, request, obj=None):
        """
        Standard change permission, return True if user has change and/or view perm if we are on object
        else return classic perm with codename
        """
        if obj is not None:
            return obj.has_change_permission(request) or obj.has_view_permission(request)
        return super(SmoothPermAdmin, self).has_change_permission(request, obj)

    def has_add_permission(self, request):
        """
        Standard add permission, return True if user has basic had permission
        """
        return super(SmoothPermAdmin, self).has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        """
        Standard delete permission, return True if user has delete perm if we are on object
        else return classic perm with codename
        """
        if obj is not None:
            return obj.has_delete_permission(request)
        return super(SmoothPermAdmin, self).has_delete_permission(request, obj)

    def remove_exclude_from_fieldsets(self, exclude, fieldsets):
        """
        Remove all exclude list in fieldsets
        :param exclude: The exlude list
        :return:
        """

        if fieldsets is not None:
            fieldsets = deepcopy(fieldsets)
            exclude = set(exclude)
            for i, key in enumerate(fieldsets):
                fields = list(key[1]['fields'])
                # We need first to remove all list to tuple, and remove exclude list in this one
                for j, field in enumerate(fields):
                    if isinstance(field, (tuple, list)):
                        field = set(field)
                        field -= exclude
                        field = tuple(field)
                    fields[j] = field

                # We get the result of for in above, and we remove exclude list on alone fields
                fields = set(fields)
                fields -= exclude
                fieldsets[i][1]['fields'] = list(fields)
        return fieldsets

    def get_queryset(self, request):
        """
        Returns a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """
        qs = super(SmoothPermAdmin, self).get_queryset(request)
        my_list = list(qs)
        for i, item in enumerate(my_list):
            if not self.has_change_permission(request, item):
                qs = qs.exclude(id=item.id)
        return qs

    def get_readonly_fields(self, request, obj=None):
        """
        Override readonly_fields. If user can only view page, all fields are readonly,
        if user hasn't advanced_settings perm, all :param:smooth_perm_field are readonly
        if user has all perms / superuser all readonly are readonly from modelAdmin
        """
        allow_fields = set()
        readonly_fields = set()
        exclude_fields = set()

        readonly_init = set(self.readonly_fields) or set()
        exclude_init = set(self.exclude_from_parent)

        if obj is not None:
            if not obj.has_change_permission(request) and obj.has_view_permission(request):
                if self.declared_fieldsets:
                    return flatten_fieldsets(self.declared_fieldsets)
                else:
                    return list(set(
                        [field.name for field in self.opts.local_fields] +
                        [field.name for field in self.opts.local_many_to_many]
                    ))
            else:
                for perm in self.smooth_perm_field:
                    value = self.smooth_perm_field[perm]

                    if self.FIELD not in value:
                        continue

                    for field in value[self.FIELD]:
                        if isinstance(field, (list, tuple)):
                            tmp = list(field)
                            field = tmp[0]
                            is_exclude = tmp[1]
                        else:
                            is_exclude = False

                        try:
                            if obj.has_smooth_permission(request, perm):
                                allow_fields.add(field)
                            elif is_exclude is True:
                                exclude_fields.add(field)
                            else:
                                readonly_fields.add(field)
                        except Exception:
                            raise PermissionNotFoundException("can_{}_permission not found" . format(perm))

                if self.model.permissions.smooth_level_perm is not self.model.permissions.HIGH_LEVEL:
                    allow_fields = allow_fields - readonly_fields - exclude_fields

            readonly_fields -= exclude_fields - allow_fields
            exclude_fields -= allow_fields

            self.exclude = list(exclude_init.union(exclude_fields))
            if len(self.exclude) > 0:
                self.fieldsets = self.remove_exclude_from_fieldsets(self.exclude, self.fieldsets_from_parent)
            else:
                self.fieldsets = list(self.fieldsets_from_parent)
            self.exclude.append('owner')

        return list(readonly_init.union(readonly_fields))

    def get_inline_classes(self, request, obj=None):
        """
        Return inlines classes with inline perms if user has change permissions perm
        :param request: request HTTP
        :param obj: obj in question
        :return: [inlines] list of inlines models
        """
        inlines = set(self.inlines) or set()
        allow_inline = set()
        deny_inline = set()

        if obj is not None:

            for perm in self.smooth_perm_field:
                value = self.smooth_perm_field[perm]

                if self.INLINE not in value:
                    continue

                for inline in value[self.INLINE]:
                    try:
                        if obj.has_smooth_permission(request, perm):
                            allow_inline.add(inline)
                        else:
                            deny_inline.add(inline)
                    except Exception:
                            raise PermissionNotFoundException("can_{}_permission not found" . format(perm))

            if self.model.permissions.smooth_level_perm is not self.model.permissions.HIGH_LEVEL:
                allow_inline = allow_inline - deny_inline

            inlines = (inlines - (deny_inline - allow_inline)).union(allow_inline)
            inlines.add(self.inline_perm_model)

            if not obj.has_change_permissions_permission(request):
                inlines.remove(self.inline_perm_model)

        return list(inlines)

    def get_inline_instances(self, request, obj=None):
        """
        Standard get_inline_instance, just update inlines, see:get_inline_classes
        """
        self.inlines = self.get_inline_classes(request, obj)
        return super(SmoothPermAdmin, self).get_inline_instances(request, obj)

    def get_fields(self, request, obj=None):
        """
        Hook for specifying fields.
        """
        return self.fields

    def get_form(self, request, obj=None, **kwargs):
        """
        Returns a Form class for use in the admin add view. This is used by
        add_view and change_view.
        """

        self.exclude = deepcopy(self.exclude_from_parent)

        self.get_readonly_fields(request, obj)
        self.get_fieldsets(request, obj)

        return super(SmoothPermAdmin, self).get_form(request, obj, **kwargs)


class SmoothPermInlineModelAdmin(InlineModelAdmin):
    INLINE = 0
    FIELD = 1

    smooth_perm_field = {}
    exclude_from_parent = ()
    fieldsets_from_parent = []


class SmoothPermStackedInline(SmoothPermInlineModelAdmin):
    template = 'admin/edit_inline/stacked.html'


class SmoothPermTabularInline(SmoothPermInlineModelAdmin):
    template = 'admin/edit_inline/tabular.html'
