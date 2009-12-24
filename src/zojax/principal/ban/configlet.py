##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from rwproperty import getproperty, setproperty
from BTrees.OOBTree import OOBTree


class BanPrincipalConfiglet(object):
    """ configlet """

    @getproperty
    def banned(self):
        banned = getattr(self.data, 'banned', None)
        if banned is not None:
            return banned
        self.data.banned = OOBTree()
        return self.data.banned

    def ban(self, uids):
        banned = self.banned
        for i in uids:
            banned[i] = i

    def unban(self, uids):
        banned = self.banned
        for i in uids:
            del banned[i]
