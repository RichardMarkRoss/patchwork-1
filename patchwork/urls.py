# Patchwork - automated patch tracking system
# Copyright (C) 2008 Jeremy Kerr <jk@ozlabs.org>
#
# This file is part of the Patchwork package.
#
# Patchwork is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Patchwork is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Patchwork; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

from django.conf import settings
from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),

    (r'^$', 'patchwork.views.project.list'),
    (r'^project/(?P<project_id>[^/]+)/list/$', 'patchwork.views.patch.list'),
    (r'^project/(?P<project_id>[^/]+)/$', 'patchwork.views.project.project'),

    # patch views
    (r'^patch/(?P<patch_id>\d+)/$', 'patchwork.views.patch.patch'),
    (r'^patch/(?P<patch_id>\d+)/raw/$', 'patchwork.views.patch.content'),
    (r'^patch/(?P<patch_id>\d+)/mbox/$', 'patchwork.views.patch.mbox'),

    # logged-in user stuff
    (r'^user/$', 'patchwork.views.user.profile'),
    (r'^user/todo/$', 'patchwork.views.user.todo_lists'),
    (r'^user/todo/(?P<project_id>[^/]+)/$', 'patchwork.views.user.todo_list'),

    (r'^user/bundles/$', 'patchwork.views.bundle.bundles'),

    (r'^user/link/$', 'patchwork.views.user.link'),
    (r'^user/unlink/(?P<person_id>[^/]+)/$', 'patchwork.views.user.unlink'),

    # password change
    url(r'^user/password-change/$', auth_views.password_change,
        name='password_change'),
    url(r'^user/password-change/done/$', auth_views.password_change_done,
        name='password_change_done'),
    url(r'^user/password-reset/$', auth_views.password_reset,
        name='password_reset'),
    url(r'^user/password-reset/mail-sent/$', auth_views.password_reset_done,
        name='password_reset_done'),
    url(r'^user/password-reset/(?P<uidb64>[0-9A-Za-z_\-]+)/'
        r'(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,
        name='password_reset_confirm'),
    url(r'^user/password-reset/complete/$',
        auth_views.password_reset_complete,
        name='password_reset_complete'),

    # login/logout
    url(r'^user/login/$', auth_views.login,
        {'template_name': 'patchwork/login.html'},
        name='auth_login'),
    url(r'^user/logout/$', auth_views.logout,
        {'template_name': 'patchwork/logout.html'},
        name='auth_logout'),

    # registration
    (r'^register/', 'patchwork.views.user.register'),

    # public view for bundles
    (r'^bundle/(?P<username>[^/]*)/(?P<bundlename>[^/]*)/$',
     'patchwork.views.bundle.bundle'),
    (r'^bundle/(?P<username>[^/]*)/(?P<bundlename>[^/]*)/mbox/$',
     'patchwork.views.bundle.mbox'),

    (r'^confirm/(?P<key>[0-9a-f]+)/$', 'patchwork.views.confirm'),

    # submitter autocomplete
    (r'^submitter/$', 'patchwork.views.api.submitters'),

    # email setup
    (r'^mail/$', 'patchwork.views.mail.settings'),
    (r'^mail/optout/$', 'patchwork.views.mail.optout'),
    (r'^mail/optin/$', 'patchwork.views.mail.optin'),

    # help!
    (r'^help/(?P<path>.*)$', 'patchwork.views.help.help'),
)

if settings.ENABLE_XMLRPC:
    urlpatterns += patterns(
        '',
        (r'xmlrpc/$', 'patchwork.views.xmlrpc.xmlrpc'),
        (r'^pwclient/$', 'patchwork.views.pwclient.pwclient'),
        (r'^project/(?P<project_id>[^/]+)/pwclientrc/$',
         'patchwork.views.pwclient.pwclientrc'),
    )

# redirect from old urls
if settings.COMPAT_REDIR:
    urlpatterns += patterns(
        '',
        (r'^user/bundle/(?P<bundle_id>[^/]+)/$',
         'patchwork.views.bundle.bundle_redir'),
        (r'^user/bundle/(?P<bundle_id>[^/]+)/mbox/$',
         'patchwork.views.bundle.mbox_redir'),
    )
