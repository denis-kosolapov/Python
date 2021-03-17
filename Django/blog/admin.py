from django.conf.global_settings import EMAIL_HOST_USER
from django.contrib import admin
from django.conf.urls import url
from django.template.response import TemplateResponse
from django.core.mail import send_mass_mail
from django import forms
from django.contrib import messages

from .models import Post
from .models import SenderEmails
from .models import Images
from .models import PageList
from .models import Contacts


class Mail(forms.ModelForm):
    class Meta():
        model = SenderEmails
        fields = ['subject', 'message']


@admin.register(SenderEmails)
class SendMassMailAdmin(admin.ModelAdmin):
    list_display = ('subject', 'date')

    def send(self, request):
        contacts = Contacts.objects.all()
        num = len(contacts)
        emails = []
        for i in range(num):
            email = contacts[i]
            emails.append(email.email)

        unique_emails = []
        for email in emails:
            if email in emails and email not in unique_emails:
                unique_emails.append(email)

        if request.method == 'POST':
            form = Mail(request.POST)
            subject = form.data['subject']
            message = form.data['message']
            send_messages = (subject, message, EMAIL_HOST_USER, unique_emails)
            if form.is_valid():
                form.save()
                messages.success(request, 'Произведена успешная рассылка')
                send_mass_mail(
                    (send_messages,), fail_silently=False
                )

    def get_urls(self):

        # get the default urls
        urls = super(SendMassMailAdmin, self).get_urls()

        # define security urls
        security_urls = [
            # url('add/', self.admin_site.admin_view(self.mass_mail)),
            url(r'^add/$', self.admin_site.admin_view(self.mass_mail))
            # Add here more urls if you want following same logic
        ]

        # Make sure here you place your added urls first than the admin default urls
        return security_urls + urls

    # Your view definition fn
    def mass_mail(self, request):
        self.send(request)
        context = dict(
            self.admin_site.each_context(request), # Include common variables for rendering the admin template.
        )
        return TemplateResponse(request, "sendmails.html", context)


class PageListAdmin(admin.ModelAdmin):
    list_display = ("url", "title", "content")


class ContactsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'date')


class SaveSenderEmailAdmin(admin.ModelAdmin):
    list_display = ('subject', 'message')


admin.site.register(PageList, PageListAdmin)
admin.site.register(Post)
admin.site.register(Images)
admin.site.register(Contacts, ContactsAdmin)
