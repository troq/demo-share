from django.conf.urls import patterns, url

from main.views import BaseTshirtList, ProfileUpdate

urlpatterns = patterns('',
    url(r'^base-tshirts/$', BaseTshirtList.as_view(), name='base-tshirt-list'),
    url(r'^base-price/$', 'main.views.base_price_view', name='base-price-view'),
    url(r'^popular-tags/$', 'main.views.popular_tags_view', name='popular-tags-view'),
    url(r'^profiles/(?P<pk>\d+)/$', ProfileUpdate.as_view(), name='profile-update'),
    url(r'^shipping/$', 'main.views.shipping_cost_view', name='shipping-list'),
)
