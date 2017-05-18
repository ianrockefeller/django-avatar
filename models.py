# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import models

class Chat(models.Model):
	name = models.CharField(max_length=255, blank=True)
	is_public = models.BooleanField()
	subscribers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return 'Chat: %s' % self.name


class Message(models.Model):
	body = models.TextField(blank=True)
	sender = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)
	chat = models.ForeignKey(Chat, blank=True, null=True, on_delete=models.CASCADE)

	def __str__(self):
	 	return "(%s) From: %s" % (self.chat.name, self.sender.username)
