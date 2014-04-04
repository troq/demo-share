from django.conf.urls import patterns, url

from main.views import TshirtPage, Designer

urlpatterns = patterns('',
    url(r'^$', 'main.views.home', name='home'),

    url(r'^designer/$', Designer.as_view(), name='designer'),

    url(r'^shop/$', 'main.views.shop', name='shop'),
    url(r'^shop/(?P<tshirt_pk>\d+)/(?:(?P<slug>[\w-]+)/)?$', TshirtPage.as_view(), name='tshirt_page'),

    url(r'^profiles/(?P<user_pk>\d+)/$', 'main.views.profile', name='profile'),

    url(r'^accounts/login/$', 'main.views.ajax_login', name='ajax_login'),
)
