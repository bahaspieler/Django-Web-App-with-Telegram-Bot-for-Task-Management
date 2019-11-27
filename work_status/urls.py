from django.conf.urls import url
from .views import *
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns =[
    url(r'^$', home, name='home'),

    url(r'^display_lte$', display_lte, name='display_lte'),
    url(r'^tool$', tool, name='tool'),
    url(r'^prs_analysis', prs_analysis, name='prs_analysis'),
    url(r'^the_team$', the_team, name='the_team'),

    url(r'^add_lte$', add_lte, name='add_lte'),
    url(r'^instance/(?P<pk>\d+)$', instance, name='instance'),

    url(r'^edit_lte/(?P<pk>\d+)$', edit_lte, name='edit_lte'),

    url(r'^delete_lte/(?P<pk>\d+)$', delete_lte, name='delete_lte'),
    url(r'^validate$', validate, name='validate'),
    path('api/button', GetList.as_view(), name='button-list'),
    path('api/text', GetFieldList.as_view(), name='text'),
    path('todo_completed/(?P<pk>\d+)$', todo_completed, name="todo_completed"),
    path('todo_pending/(?P<pk>\d+)$', todo_pending, name="todo_pending"),
    path('^download/(?P<path>.*)/(?P<file_name>.*)$', download, name='download')

    # path('api/catag', EntryCatagory.as_view(), name='text'),

]

# if settings.DEBUG:
#     urlpatterns = url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT, 'show_indexes': True})  + urlpatterns
