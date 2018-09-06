from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Album, Song
from .forms import UserForm


class IndexView(generic.ListView):
    template_name = 'music/index.html'
    context_object_name = 'albums'  # default is `object_list`

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(IndexView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Album.objects.filter(user=self.request.user)


class SongView(generic.ListView):
    template_name = 'music/song.html'
    context_object_name = 'songs'  # default is `object_list`

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SongView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        songs = Song.objects.filter(album__user=self.request.user)
        if self.kwargs.get('filter') == 'favorites':
            songs = songs.filter(is_favourite=True)
        return songs

    def get_context_data(self, **kwargs):
        context = super(SongView, self).get_context_data(**kwargs)
        context['filter_by'] = self.kwargs.get('filter', 'all')
        return context


class DetailView(generic.DetailView):
    model = Album
    template_name = 'music/detail.html'
    context_object_name = 'album'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DetailView, self).dispatch(request, *args, **kwargs)


class AlbumCreate(CreateView):
    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_logo', 'is_favourite']
    # Default template name to be called is album_form.html (<modelname_form.html>)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AlbumCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class SongCreate(CreateView):
    model = Song
    fields = ['file_type', 'song_title', 'is_favourite']
    # Default template name to be called is album_form.html (<modelname_form.html>)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SongCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.album = get_object_or_404(Album, pk=self.kwargs.get('album_id'))
        return super().form_valid(form)


class SongDelete(DeleteView):
    model = Song
    # success_url = reverse_lazy('music:detail')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SongDelete, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        album_id = self.kwargs.get('album_id')
        return reverse_lazy('music:detail', kwargs={'pk': album_id})


class SongUpdate(UpdateView):
    model = Song
    fields = ['file_type', 'song_title', 'is_favourite']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SongUpdate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        album_id = self.kwargs.get('album_id')
        return reverse_lazy('music:detail', kwargs={'pk': album_id})


class AlbumUpdate(UpdateView):
    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_logo', 'is_favourite']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AlbumUpdate, self).dispatch(request, *args, **kwargs)


class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AlbumDelete, self).dispatch(request, *args, **kwargs)


class UserFormView(View):
    form_class = UserForm
    template_name = 'registration/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # Just if we want to clean of change some data before saving...
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # if password is required to be changed, pass like this and make sure to hash it first
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect('music:index')

        return render(request, self.template_name, {'form': form})


class FavouriteAlbum(View):

    def get(self, request, pk):
        album = get_object_or_404(Album, pk=pk)
        album.is_favourite = True
        album.save()
        return redirect('music:index')


class FavouriteSong(View):

    def get(self, request, pk):
        song = get_object_or_404(Song, pk=pk)
        song.is_favourite = True
        song.save()
        return redirect('music:songs', 'all')


def handler404(request, exception):
    return render(request, 'errors/404.html', locals())
