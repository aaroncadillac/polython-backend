from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from stores import views
 
 
urlpatterns = [
	url(r'^stores/create/$', views.CreateStore.as_view(), name='store-create'),
    url(r'^stores/(?P<pk>[0-9a-f-]+)/$', views.StoreDetail.as_view(), name='store-detail'),
    url(r'^stores/products/add/$', views.AddProducts.as_view(), name='store-add-products'),
    url(r'^stores/list/$', views.UserStores.as_view(), name='store-list'),
]