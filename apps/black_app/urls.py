from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^main$', views.main, name='main'),
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^appointments$', views.appointments, name='appointments'),
    url(r'^appointmens/add$', views.add, name = 'add'),
    # url(r'^wish_items/(?P<id>\d+)$', views.wish_items),
    # url(r'^wish_items/add/$', views.add),
    url(r'^appointments/(?P<id>\d+)$', views.edit, name = 'edit'),
    url(r'^appointments/delete/(?P<id>\d+)$', views.delete_app, name = 'delete'),
    url(r'^appointments/update$', views.update_app, name = 'update'),
]
