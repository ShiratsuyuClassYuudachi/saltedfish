import json
import time
import uuid

from django.http import HttpResponse

from user.models import User
from .models import Message, MessageList


def send(request):
    if request.session.get("uuid") is not None:
        if User.objects.filter(uuid=uuid.UUID(request.session.get("uuid"))).exists():
            data = json.load(request.body)
            receiver = data.receiver
            sender = uuid.UUID(request.session.get("uuid"))
            if MessageList.objects.filter(receiver=receiver, sender=sender):
                messagelist = MessageList.objects.get(receiver=receiver, sender=sender)
                messagelist.receiverRead = False
            elif MessageList.objects.filter(receiver=sender, sender=receiver):
                messagelist = MessageList.objects.get(receiver=sender, sender=receiver)
                messagelist.senderRead = False
            else:
                messagelist = MessageList.objects.__new__()
                messagelist.sender = sender
                messagelist.receiver = receiver
                messagelist.UUID = uuid.uuid4()
                messagelist.senderRead = True
                messagelist.receiverRead = False
            message = Message.objects.__new__()
            if data.type is 0:
                message.type = 0
                message.content = data.content
            else:
                message.type = 1
                message.image = data.content
            message.time = time.time()
            message.sender = sender
            message.UUID = uuid.uuid4()
            message.save()
            messagelist.messages.append(message.UUID)
            messagelist.save()
            recv = User.objects.get(uuid=receiver)
            if recv.messageList.count(messagelist.UUID) != 0:
                recv.messageList.remove(messagelist.UUID)
            sen = User.objects.get(uuid=sender)
            if sen.messageList.count(messagelist.UUID) != 0:
                sen.messageList.remove(messagelist.UUID)
            recv.messageList.append(messagelist)
            sen.messageList.append(messagelist)
            recv.save()
            sen.save()
            return HttpResponse(status=201)
    return HttpResponse("unauthenticated", status=401)


def getlist(request):
    if request.session.get("uuid") is not None:
        if User.objects.filter(uuid=uuid.UUID(request.session.get("uuid"))).exists():
            user = uuid.UUID(request.session.get("uuid"))
            if MessageList.objects.filter(sender=user).exists():
                messagelist = MessageList.objects.get(sender=user)
                last = messagelist.messages.pop()
                messagelist.append(last)
                message = Message.objects.get(UUID=last)
                if message.type is 0:
                    content = message.content
                else:
                    content = '[image]'
                rep = {
                    'time': messagelist.time,
                    'sender': messagelist.receiver,
                    'isRead': messagelist.senderRead,
                    'content': content
                }
                return HttpResponse(json.dumps(rep), status=200)
            elif MessageList.objects.filter(receiver=user).exists():
                messagelist = MessageList.objects.get(receiver=user)
                last = messagelist.messages.pop()
                messagelist.append(last)
                message = Message.objects.get(UUID=last)
                if message.type is 0:
                    content = message.content
                else:
                    content = '[image]'
                rep = {
                    'time': messagelist.time,
                    'sender': messagelist.sender,
                    'isRead': messagelist.receiverRead,
                    'content': content
                }
                return HttpResponse(json.dumps(rep), status=200)
            else:
                return HttpResponse(status=403)
    return HttpResponse("unauthenticated", status=401)


def getdetial(request):
    if request.session.get("uuid") is not None:
        if User.objects.filter(uuid=uuid.UUID(request.session.get("uuid"))).exists():
            user = uuid.UUID(request.session.get("uuid"))
            if MessageList.objects.filter(sender=user).exists():
                messagelist = MessageList.objects.get(sender=user)
                messagelist.senderRead = True
                messagelist.save()
                rep = {
                    'messages': messagelist.messages
                }
                return HttpResponse(json.dumps(rep), status=200)
            elif MessageList.objects.filter(receiver=user).exists():
                messagelist = MessageList.objects.get(sender=user)
                messagelist.receiverRead = True
                messagelist.save()
                rep = {
                    'messages': messagelist.messages
                }
                return HttpResponse(json.dumps(rep), status=200)
            else:
                return HttpResponse(status=403)
    return HttpResponse("unauthenticated", status=401)


def getmessage(request):
    if request.session.get("uuid") is not None:
        if User.objects.filter(uuid=uuid.UUID(request.session.get("uuid"))).exists():
            user = uuid.UUID(request.session.get("uuid"))
            message = Message.objects.get(UUID=request.GET.get('messageid'))
            if message.sender == user:
                if message.type == 0:
                    rep = {
                        'source': 'from',
                        'type': 'text',
                        'content': message.content
                    }
                else:
                    rep = {
                        'source': 'from',
                        'type': 'img',
                        'content': message.image
                    }
            else:
                if message.type == 0:
                    rep = {
                        'source': 'to',
                        'type': 'text',
                        'content': message.content
                    }
                else:
                    rep = {
                        'source': 'to',
                        'type': 'img',
                        'content': message.image
                    }
            HttpResponse(json.dumps(rep), status=200)
    return HttpResponse("unauthenticated", status=401)

# Create your views here.
