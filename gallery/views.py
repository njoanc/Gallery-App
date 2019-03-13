from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .forms import *
from pusher import Pusher
import json

    #instantiate pusher
    pusher = Pusher(app_id=u'XXX_APP_ID', key=u'XXX_APP_KEY', secret=u'XXX_APP_SECRET', cluster=u'XXX_APP_CLUSTER')
    # Create your views here.
    # function that serves the welcome page
    def index(request):
        # get all current photos ordered by the latest
        all_documents = Gallery.objects.all().order_by('-id')
        # return the index.html template, passing in all the gallery
        return render(request, 'index.html', {'all_documents': all_documents})

    #function that authenticates the private channel 
    def pusher_authentication(request):
        channel = request.GET.get('channel_name', None)
        socket_id = request.GET.get('socket_id', None)
        auth = pusher.authenticate(
          channel = channel,
          socket_id = socket_id
        )

        return JsonResponse(json.dumps(auth), safe=False)
    #function that triggers the pusher request
    def push_gallery(request):
        # check if the method is post
        if request.method == 'POST':
            # try form validation
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                f = form.save()
                # trigger a pusher request after saving the new gallery element 
                pusher.trigger(u'a_channel', u'an_event', {u'description': f.description, u'document': f.document.url})
                return HttpResponse('ok')
            else:
                # return a form not valid error
                return HttpResponse('form not valid')
        else:
           # return error, type isnt post
           return HttpResponse('error, please try again')