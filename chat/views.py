import secrets

from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


def index(request):
    return render(request, 'chat/index.html', {})


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })


@csrf_exempt
@require_http_methods(["POST", ])
@login_required
def websocket_token(request, room_name):
    token = secrets.token_urlsafe(16)
    cache.set(f'{token}', request.user.id)
    return JsonResponse(dict(token=token))
