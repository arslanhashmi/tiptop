from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


app_name = 'music'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.UserFormView.as_view(), name='register'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('songs/<str:filter>/', views.SongView.as_view(), name='songs'),
    path('album/add/', views.AlbumCreate.as_view(), name='add_album'),
    path('album/<int:pk>/', views.AlbumUpdate.as_view(), name='update_album'),
    path('album/<int:pk>/delete/', views.AlbumDelete.as_view(), name='delete_album'),
    path('<int:pk>/favourite/', views.FavouriteAlbum.as_view(), name='favourite_album'),
    path('songs/<int:pk>/favourite/', views.FavouriteSong.as_view(), name='favourite_song'),
    path('songs/<int:album_id>/create/', views.SongCreate.as_view(), name='create_song'),
    path('songs/<int:album_id>/<int:pk>/delete/', views.SongDelete.as_view(), name='delete_song'),
    path('songs/<int:album_id>/<int:pk>/update/', views.SongUpdate.as_view(), name='edit_song'),
]
