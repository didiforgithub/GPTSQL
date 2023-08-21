from django.urls import re_path as url

from . import views


urlpatterns =[
    url(r'^API1/$', views.get_table_name),
    url(r'^API2/$', views.gpt_sql),
    url(r'^API3/$', views.Info_get),
    url(r'^API4/$',views.zero_info_get)
]