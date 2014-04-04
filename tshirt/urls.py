from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('main.urls', namespace='main')),

    url(r'^accounts/logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': settings.LOGOUT_REDIRECT_URL},
        name='custom_auth_logout'),
    url(r'^accounts/', include('custom_registration_backend.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url(r'^api/', include('main.api_urls', namespace='main-api')),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
