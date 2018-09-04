from django.urls import path

from . import views


app_name = 'music'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('album/add/', views.AlbumCreate.as_view(), name='add_album'),
    path('album/<int:pk>/', views.AlbumUpdate.as_view(), name='update_album'),
    path('album/<int:pk>/delete/', views.AlbumDelete.as_view(), name='delete_album'),
    # path('<int:album_id>/favourite/', views.favourite, name='favourite'),
]
