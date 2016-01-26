from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group, User
from django.conf import settings
from django.contrib.auth import get_permission_codename
from smooth_perms.managers import GlobalPermissionManager


class SmoothGroup(Group):
    class Meta:
        verbose_name = _(u'User group (SmoothPerm)')
        verbose_name_plural = _(u'User groups (SmoothPerm)')


class SmoothUser(User):
    class Meta:
        verbose_name = _(u'User (SmoothPerm)')
        verbose_name_plural = _(u'Users (SmoothPerm)')


class ModelPermission(models.Model):

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owned_%(class)ss', verbose_name=_("owner"), blank=True, null=True)

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    modified_at = models.DateTimeField(_('modified at'), auto_now=True)

    smooth_perm_change_all = False
    smooth_perm_delete_all = False

    def has_smooth_permission(self, request, permission_type):
        if hasattr(self, "has_{}_permission" . format(permission_type)):
            return getattr(self, "has_{}_permission" . format(permission_type))(request)
        return getattr(self, "has_generic_permission" . format(permission_type))(request, permission_type)

    def has_generic_permission(self, request, permission_type):
        """
        Return True if user in :param:request has :param:permission_type
        :param request: The request http
        :param permission_type: the codename of permission
        :return: bool. True if user has permission
        """
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

    def has_delete_permission(self, request, user=None):
        """
        Return True if user in :param:request has delete permission
        :param request: The request http
        :return: bool. True if user has delete permission
        """
        opts = self._meta
        if not user:
            user = request.user
        if user.is_superuser:
            return True
        return ((user.has_perm(opts.app_label + '.' + get_permission_codename('delete', opts)) and self.smooth_perm_delete_all)
                or (user.has_perm(opts.app_label + '.' + get_permission_codename('delete', opts)) and self.has_generic_permission(request, "delete")))

    def has_change_permission(self, request, user=None):
        """
        Return True if user in :param:request has change permission
        :param request: The request http
        :return: bool. True if user has change permission
        """
        opts = self._meta
        if not user:
            user = request.user
        if user.is_superuser:
            return True
        return ((user.has_perm(opts.app_label + '.' + get_permission_codename('change', opts)) and self.smooth_perm_change_all)
                or (user.has_perm(opts.app_label + '.' + get_permission_codename('change', opts)) and self.has_generic_permission(request, "change")))

    def has_advanced_settings_permission(self, request):
        """
        Return True if user in :param:request has advanced_settings permission
        :param request: The request http
        """
        return self.has_generic_permission(request, "advanced_settings")

    def has_change_permissions_permission(self, request):
        """
        Return True if user in :param:request has change permissions permission
        :param request: The request http
        :return: bool. True if user has change permissions permission
        """
        return self.has_generic_permission(request, "change_permissions")

    def has_delete_permissions_permission(self, request):
        """
        Return True if user in :param:request has delete permissions permission
        :param request: The request http
        :return: bool. True if user has delete permissions permission
        """
        return self.has_generic_permission(request, "delete_permissions")

    def has_view_permission(self, request):
        """
        Return True if user in :param:request has view permission
        :param request: The request http
        :return: bool. True if user has view permission
        """
        return self.has_generic_permission(request, "view")

    class Meta:
        abstract = True


class GlobalPermissionMixin(models.Model):
    """
    Class for global permission :
    Default permission = (
            'change',
            'delete',
            'advanced_settings',
            'change_permissions',
            'delete_permissions',
            'view',
        )
    For add new one :
        Create a model with inheritance, add boolean field with this name syntaxe can_%s where %s is the permission
        And add this permission in PERMISSIONS constant for automatically update admin view
    """
    PERMISSIONS = ()

    LOW_LEVEL = 0
    HIGH_LEVEL = 1

    smooth_level_perm = LOW_LEVEL

    def __init__(self, *args, **kwargs):
        self.PERMISSIONS = self.PERMISSIONS + (
            'change',
            'delete',
            'advanced_settings',
            'change_permissions',
            'delete_permissions',
            'view',
        )
        super(GlobalPermissionMixin, self).__init__(*args, **kwargs)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("user"), blank=True, null=True)
    group = models.ForeignKey(Group, verbose_name=_("group"), blank=True, null=True)

    can_change = models.BooleanField(_("can edit"), default=False)
    can_advanced_settings = models.BooleanField(_("can change advanced settings"), default=False)

    can_delete = models.BooleanField(_("can delete"), default=False)

    can_change_permissions = models.BooleanField(_("can change permissions"), default=False)
    can_delete_permissions = models.BooleanField(_("can delete permissions"), default=False)

    can_view = models.BooleanField(_("view restricted"), default=False)

    objects = GlobalPermissionManager()

    class Meta:
        abstract = True
