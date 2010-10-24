from django.contrib import admin
from django.conf.urls.defaults import *
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.template.defaultfilters import truncatewords

from feedback.models import Feedback

class FeedbackAdmin(admin.ModelAdmin):
    
    def view(self, obj):
        return "<a href='%s'>View</a>" % obj.get_absolute_url()
    view.allow_tags = True

    def feedback(self, obj):
        return truncatewords(obj.message, 15)
    
    list_display = ['user', 'feedback', 'time', 'type', 'page', 'view']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'message', 'page']
    list_filter = ['type', 'time']
    
    def get_urls(self):
        urls = super(FeedbackAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^view/(?P<feedback_id>\d+)/$', self.admin_site.admin_view(self.view_feedback), name='view-feedback'),
        )
        return my_urls + urls
        
    def view_feedback(self, request, feedback_id):
        feedback = get_object_or_404(Feedback, id=feedback_id)
        return render_to_response('feedback/view_feedback.html',
            {'feedback': feedback}, context_instance=RequestContext(request))

admin.site.register(Feedback, FeedbackAdmin)

admin.site.index_template = 'feedback/index.html'
