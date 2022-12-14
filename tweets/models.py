from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from utils.time_helpers import utc_now

# Create your models here.
class Tweet(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL,
                             null=True,
                             help_text='who posts the tweet',
                             )
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # need to make migration if new index is added
        index_together = (('user', 'created_at'),)

    @property
    def hours_to_now(self):
        # can't call datetime.now() because self.created_at has timezone info
        # but datetime.now() doesn't. And it will throw an error
        return (utc_now() - self.created_at).seconds // 3600

    def __str__(self):
        return f'{self.created_at} {self.user}: {self.content}'
