from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.mail import BadHeaderError, send_mail
from django.contrib import messages

class HomePage(View):
    template = 'website/index.html'

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        subject = 'ptpmap'
        name = request.POST.get('name', '')
        from_email = request.POST.get('email', '')
        city = request.POST.get('email', '')
        message = request.POST.get('message', '')

        if name and from_email and city:
            try:
                send_mail(subject, 'Name: '+name + ' City: ' + city + ' Message: '+ message, from_email, ['support@drive-software.com'])
            except BadHeaderError:
                messages.error(request, 'Съобщение НЕ е доставено')
                return HttpResponseRedirect(reverse('homepage') + '#member')
            messages.success(request, 'Съобщение е доставено')
            return HttpResponseRedirect(reverse('homepage') + '#member')
        else:
            messages.error(request, 'Съобщение НЕ е доставено')
            return HttpResponseRedirect(reverse('homepage') + '#member')
