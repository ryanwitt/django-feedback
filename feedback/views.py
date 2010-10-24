from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages

from feedback.forms import FeedbackForm

def leave_feedback(request, message='Thanks for your feedback!', message_level=messages.SUCCESS):
    form = FeedbackForm(request.POST or None)
    if form.is_valid():
        feedback = form.save(commit=False)
        if request.user.is_authenticated():
            feedback.user = request.user
            messages.add_message(request, message_level, message)
        feedback.save()
        return HttpResponseRedirect(request.POST.get('next', request.META.get('HTTP_REFERER', '/')))
    return render_to_response('feedback/feedback_form.html', {'form': form}, context_instance=RequestContext(request))
