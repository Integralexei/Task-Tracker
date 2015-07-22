from django.conf.urls import url, patterns

urlpatterns = patterns('',
                       url(r'^login', 'loginsys.views.login'),
                       url(r'^logout', 'loginsys.views.logout'),
                       url(r'^register_success', 'loginsys.views.register_success'),
                       url(r'^register', 'loginsys.views.register'),
                       url(r'^login/activation_key/', 'loginsys.views.register_confirm'),
# url(r'^articles/addcomment/(?P<article_id>\d+)/$', 'article.views.addcomment'),

                       )
from django.conf.urls import patterns, include, url

# from django.contrib import admin
# admin.autodiscover()
#
# urlpatterns = patterns('',
#     url(r'^sign_up/', ('yourappname.views.register_user')),
#     url(r'^register_success/', ('yourappname.views.register_success')),
#     url(r'^confirm/(?P\w+)/', ('yourappname.views.register_confirm')),
# )