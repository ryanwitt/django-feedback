===============
django-feedback
===============

Django Feedback is a simple Django application that makes it trivialto start accepting user feedback 
from authenticated users within your Django project.

Installation
============

Put ``feedback`` in your ``INSTALLED_APPS``, and set ``FEEDBACK_CHOICES`` to a 2-tuple of feedback types
in your settings file. For example::

	FEEDBACK_CHOICES = (
		('bug', 'Bug'),
		('feature_request', 'Feature Request)
	)
	
Also, be sure to include ``feedback.urls`` somewhere in your urls.py file.

Add ``feedback.context_processors.feedback_form`` to ``TEMPLATE_CONTEXT_PROCESSORS``, and
``feedback_form`` will be in the context for all authenticated users.

Email Feedback
==============

If you want to recieve an email when a user leaves feedback, add the following
to your settings file::

    FEEDBACK_SENDS_EMAIL = True

The Reply-To address is set to the user's email so you can quickly respond.

By default, this sends feedback emails to everybody in ``ADMINS``, but you can
change this if you want::

    FEEDBACK_RECIPIENTS = MANAGERS
    # or explicitly
    FEEDBACK_RECIPIENTS = (
        ('Django Pony', 'pony@example.com'),
        ('Joe Schmoe', 'joe@example.com'),
    )

In addition to your usual ``EMAIL_SUBJECT_PREFIX``, feedback adds its own
prefix, ``FEEDBACK_SUBJECT_PREFIX`` which defaults to ``[feedback]``.

The templates for feedback emails (which you may override) are:

    feedback/email-subject.txt
    feedback/email.txt


Screenshots
===========
.. image:: https://cloud.github.com/downloads/girasquid/django-feedback/django-feedback-1.PNG

Overview in your admin index. Allows you to see all feedback current in the system.

.. image:: http://cloud.github.com/downloads/girasquid/django-feedback/django-feedback-2.PNG

Viewing a piece of feedback from a user.
