# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
# from django.contrib.auth.models import User
from .models import Chat, Message

def index(request):
  context = {}

  if request.user.is_authenticated:
  	context['username'] = request.user.username
  else:
  	context['username'] = ''

  chats = Chat.objects.filter().values_list('id', flat=True)

  context['chats'] = chats
  
  return render(request, 'weaver/index.html', context)

def public_chat(request, chat):
  context = {}
  return render(request, 'weaver/channel.html', context)

def private_chat(request, chat):
  context = {
    'chat_id': chat.id,
  }

  return render(request, 'weaver/chat.html', context)

def chat(request, chat_id):
  chat = Chat.objects.get(id=chat_id)

  if chat:
    if chat.is_public:
      return public_chat(request, chat)
    else:
      return private_chat(request, chat)

