from django.test import TestCase as DjangoTestCase
from django.contrib.auth.models import User
from tweets.models import Tweet

class TestCase(DjangoTestCase):

    def create_user(self, username, email=None, password=None):
        if password is None:
            password = 'password'
        if email is None:
            email = f'{username}@test.com'
        return User.objects.create_user(username, email, password)

    def create_tweet(selfself, user, content=None):
        if content is None:
            content = ''
        return Tweet.objects.create(user=user, content=content)