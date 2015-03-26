from django.conf.urls import patterns, url
from gpp import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^index/', views.index, name='index'),
        url(r'^results/', views.results, name='results'),
        url(r'^publication/', views.publication, name='publication')
)
