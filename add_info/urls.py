from django.conf.urls import url
from django.urls import path
from django.views.static import serve

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('', views.index, name='index'),
                  url(r'^select_category$', views.add_info, name='new_info'),
                  url(r'^add_data/(?P<category_id>.*)/(?P<type>.*)$', views.add_data, name='add_data'),
                  url(r'^check_data/$', views.check_data, name='check_data'),
                  url(r'^added_succesfully/$', views.added_succesfully, name='added_succesfully'),
                  url(r'^profile/$', views.profile, name='profile'),
                  url(r'^user_info/$', views.user_info, name='user_info'),
                  url(r'^select_recommend/$', views.select_recommend, name='select_recommend'),
                  url(r'^list_of_rec/$', views.list_of_rec, name='list_of_rec')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
