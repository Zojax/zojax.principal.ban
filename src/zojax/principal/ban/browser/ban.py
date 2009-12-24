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
from zope.component import getUtility
from zope.traversing.browser import absoluteURL
from zope.security.proxy import removeSecurityProxy
from zope.app.security.interfaces import IAuthentication, PrincipalLookupError

from zojax.batching.batch import Batch
from zojax.layoutform import interfaces, button, Fields, PageletForm
from zojax.principal.profile.interfaces import IPersonalProfile
from zojax.statusmessage.interfaces import IStatusMessage

from interfaces import _, IBanPrincipalsForm


class BanPrincipalsForm(PageletForm):

    title = _(u'Manage')
    fields = Fields(IBanPrincipalsForm)
    ignoreContext = True

    def update(self):
        super(BanPrincipalsForm, self).update()

        self.auth = getUtility(IAuthentication)
        self.banned = removeSecurityProxy(self.context.banned)
        self.batch = Batch(
            self.banned.keys(), size=30,
            context=self.context, request=self.request)

    def getMemberInfo(self, id):
        try:
            principal = self.auth.getPrincipal(id)
        except PrincipalLookupError:
            return

        profile = IPersonalProfile(principal)

        space = profile.space
        if space is not None:
            space = u'%s/profile/'%absoluteURL(space, self.request)

        info = {'id': principal.id,
                'space': space,
                'title': profile.title,
                'avatar': profile.avatarUrl(self.request)}
        return info

    @button.buttonAndHandler(_(u'Ban'), provides=interfaces.IAddButton)
    def handleBan(self, action):
        request = self.request
        data, errors = self.extractData()

        if not data['principals']:
            IStatusMessage(request).add(
                _(u'Please select member.'), 'warning')
            return

        self.context.ban(data['principals'])

        IStatusMessage(request).add(_(u'Members has been banned.'))
        self.redirect('.')

    @button.buttonAndHandler(_(u'Unban'), provides=interfaces.ICancelButton)
    def handleUnban(self, action):
        request = self.request
        data, errors = self.extractData()

        uids = request.get('principal.users', ())

        if not uids:
            IStatusMessage(request).add(
                _(u'Please select members.'), 'warning')
            return

        self.context.unban(uids)

        IStatusMessage(request).add(_(u'Members have been unbanned.'))
        self.redirect('.')
