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
from zope import interface, component
from zope.component import getUtility
from zope.security.management import queryInteraction

from zojax.authentication.interfaces import \
    IPrincipalInitializedEvent, PrincipalInitializationFailed
from zojax.statusmessage.interfaces import IStatusMessage

from interfaces import _, IBanPrincipalConfiglet


@component.adapter(IPrincipalInitializedEvent)
def principalInitialized(event):
    configlet = getUtility(IBanPrincipalConfiglet)
    if event.principal.id in configlet.banned:
        raise PrincipalInitializationFailed(_(u'Your account is banned.'))
