from django.shortcuts import render


def index(request):
    return render(request, 'sentence_game/index.html')


def room(request, room_name):
    return render(request, 'sentence_game/room.html', {
        'room_name': room_name
    })
