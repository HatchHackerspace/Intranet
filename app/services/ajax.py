from app.users.models import Users
from app.messages.models import Messages
from flask import g,json
import datetime,random,string


def getajax(value):
    if value == 'usernames':
        return [str(x.username) for x in Users.objects(status=True)]


def getnewmessages(id):
    return Messages.objects(ownerid=g.user,read=False).count()


def generate_msgid(size=8,chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size)) + datetime.datetime.now().strftime('%d%m%Y%M%S%f')