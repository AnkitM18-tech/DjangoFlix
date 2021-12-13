from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import RatingForm
from .models import Rating
from django.contrib.contenttypes.models import ContentType

def rate_object_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            object_id = form.cleaned_data.get('object_id')
            rating = form.cleaned_data.get('rating')
            content_type_id = form.cleaned_data.get('content_type_id')
            c_type = ContentType.objects.get_for_id(content_type_id)
            obj= Rating.objects.create(
                content_type=c_type,
                object_id = object_id,
                value=rating,
                user=request.user,
            )
            next = form.cleaned_data.get('next')
            return HttpResponseRedirect(next)
    return HttpResponseRedirect('/')