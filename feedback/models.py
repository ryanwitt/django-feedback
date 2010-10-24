from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings

class Feedback(models.Model):

    class Meta:

        ordering = ['-time']

    user    = models.ForeignKey(User, blank=True, null=True)
    type    = models.CharField(choices=settings.FEEDBACK_CHOICES, max_length=100, default=settings.FEEDBACK_CHOICES[0][0])
    message = models.TextField()
    time    = models.DateTimeField(auto_now_add=True)
    page    = models.CharField(max_length=1024, null=True, blank=True)

    def __unicode__(self):
        return self.message

    def get_absolute_url(self):
        return reverse('admin:view-feedback', args=[self.id])
