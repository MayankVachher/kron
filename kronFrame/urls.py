from django.conf.urls import url

from . import views

app_name = 'kronFrame'
urlpatterns = [
	url(r'^inDev/', views.IndexView.as_view(), name='index'),
	url(r'^$', views.HomeView.as_view(), name='home'),
        url(r'^subgraph/', views.subgraph, name='subgraph'),
]
