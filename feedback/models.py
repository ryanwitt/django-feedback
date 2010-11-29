from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings
from django.template.loader import render_to_string
from django.forms.models import model_to_dict
from django.core.mail import get_connection
from django.core.mail.message import EmailMessage

if not hasattr(settings, 'FEEDBACK_RECIPIENTS'):
    settings.FEEDBACK_RECIPIENTS = settings.ADMINS
if not hasattr(settings, 'FEEDBACK_SUBJECT_PREFIX'):
    settings.FEEDBACK_SUBJECT_PREFIX = '[feedback]'

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

    def user_specific_id(self):
        """
        Returns a number for this feedback that is unique for
        the feedback type and feedback user.
        """
        return Feedback.objects.filter(
            type = self.type, 
            user = self.user,
            time__lte = self.time,
        ).count()

    def send_feedback_email(self):
        """
        Sends a feedback email to FEEDBACK_RECIPIENTS.
        """
        context = {'feedback': self}
        context.update({'settings': settings})

        subject = render_to_string(
            'feedback/email-subject.txt', context
        )
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())

        message = render_to_string(
            'feedback/email.txt', context,
        )

        recipient_list = [a[1] for a in settings.FEEDBACK_RECIPIENTS]

        connection = get_connection()
        return EmailMessage(
            subject, message, self.user.email, recipient_list, 
            headers = {'Reply-To': self.user.email},
            connection = connection,
        ).send()

