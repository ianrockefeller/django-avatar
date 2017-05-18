from channels import Group, Channel
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http
from .models import Message, Chat
from django.contrib.auth.models import User


def msg_consumer(message):
	chat = message.content['chat']

	Message.objects.create(
		body=message.content['message'],
		sender=User.objects.get(id=int(message.content['user_id'])),
		chat=Chat.objects.get(id=int(chat)),
	)

	Group('chat-%s' % chat).send({
		'text': message.content['message'],
	})

# websocket.connect
@channel_session_user_from_http
def ws_connect(message):
	chat = message.content['path'].strip("/")
	message.channel_session['chat'] = chat
	Group('chat-%s' % chat).add(message.reply_channel)
	message.reply_channel.send({'accept': True})

# websocket.receive
@channel_session_user
def ws_message(message):
	print(message.user.id)
	Channel('chat-messages').send({
		'chat': message.channel_session['chat'],
		'message': message['text'],
		'user_id': message.user.id,
	})

# websocket.disconnect
@channel_session
def ws_disconnect(message):
	Group('chat-%s' % message.channel_session['chat']).discard(message.reply_channel)
