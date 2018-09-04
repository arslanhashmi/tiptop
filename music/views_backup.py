from django.shortcuts import render, get_object_or_404

from .models import Album, Song


def index(request):
    albums = Album.objects.all()
    context = {
        'albums': albums
    }
    return render(request, 'music/index.html', context)


def detail(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    return render(request, 'music/detail.html', {'album': album})


def favourite(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    context = {'album': album}
    try:
        selected_song = album.song_set.get(pk=request.POST['song'])
        selected_song.is_favourite = True
        selected_song.save()
    except (KeyError, Song.DoesNotExist):
        context['error_msg'] = "Please select a valid song"
    return render(request, 'music/detail.html', context)