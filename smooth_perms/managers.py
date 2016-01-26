# -*- coding: utf-8 -*-
"""
..module:managers
    :project: 
    :platform: Unix
    :synopsis: Module for core database specification, created on 28/03/2015 

..moduleauthor:: Jean-Baptiste Munieres <jbaptiste.munieres@gmail.com>

"""
from django.db import models
from django.db.models import Q


class PermissionNotFoundException(Exception):
    pass


class GlobalPermissionManager(models.Manager):
    """
    Class for  permissions management

    :param foreign_key : The foreign key from the permission model
    :type str.
    """
    foreign_key = ""

    @staticmethod
    def get_grant_all():
        """
        Return the constant when user have all rights
        :return "All"
        """
        return 'All'

    def get_smooth_id_list(self, user, perm):
        if hasattr(self, "get_{}_id_list" . format(perm)):
            return getattr(self, "get_{}_id_list" . format(perm))(user)
        return getattr(self, "get_generic_id_list" . format(perm))(user, perm)

    def get_generic_id_list(self, user, perm):
        return self.__get_id_list(user, "can_{}" .format(perm))

    def get_publish_id_list(self, user):
        """
        Give a list of object where the user has publish rights or the string "All" if
        the user has all rights.
        """
        return self.__get_id_list(user, "can_publish")

    def get_change_id_list(self, user):
        """
        Give a list of object where the user has edit rights or the string "All" if
        the user has all rights.
        """
        return self.__get_id_list(user, "can_change")

    def get_add_id_list(self, user):
        """
        Give a list of object where the user has add object rights or the string
        "All" if the user has all rights.
        """
        return self.__get_id_list(user, "can_add")

    def get_delete_id_list(self, user):
        """
        Give a list of object where the user has delete rights or the string "All" if
        the user has all rights.
        """
        return self.__get_id_list(user, "can_delete")

    def get_advanced_settings_id_list(self, user):
        """
        Give a list of object where the user can change advanced settings or the
        string "All" if the user has all rights.
        """
        return self.__get_id_list(user, "can_advanced_settings")

    def get_change_permissions_id_list(self, user):
        """Give a list of object where the user can change permissions.
        """
        return self.__get_id_list(user, "can_change_permissions")

    def get_delete_permissions_id_list(self, user):
        """Give a list of object where the user can change permissions.
        """
        return self.__get_id_list(user, "can_delete_permissions")

    def get_view_id_list(self, user):
        """Give a list of objects which user can view.
        """
        return self.__get_id_list(user, "can_view")

    def __get_id_list(self, user, attr):
        """
        Git the list of id, where :param:user have :param:attr permission
        :param user: The user
        :param attr: The codename for permission
        :return:[int] of id
        """
        if user.is_superuser:
            return self.get_grant_all()
        allow_list = set()
        deny_list = set()
        group_ids = user.groups.all().values_list('id', flat=True)
        q = Q(user=user) | Q(group__in=group_ids)
        perms = self.filter(q)

        for perm in perms:
            p = getattr(perm, attr)
            if p is None:
                # Not allow nor deny, we continue with the next permission
                continue

            obj_id = getattr(perm, self.foreign_key).id

            # TODO : Add func here for children case

            if p is True:
                allow_list.add(obj_id)
            else:
                deny_list.add(obj_id)

        if self.model.smooth_level_perm is self.model.HIGH_LEVEL:
            return allow_list
        else:
            return allow_list - deny_list