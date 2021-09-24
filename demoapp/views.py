from django.shortcuts import render

# Create your views here.
from .models import postandcomment
from .generate import generate_comment, ner, detect_category

def index(request):

    # As we are passing these data to html, if not referenced beforehand, it will throw exception
    # local variable '----' referenced before assignment
    formdata = None

    # Check for 'POST' method
    if request.method == 'POST':
        
        # Get the post
        post = request.POST.get('post')

        # Genearate a comment if not a blank post
        if post.strip()!='':
            # Find the entities and detect them (returns a dictionary)
            ner_dict = ner(post)

            # Detect the category of the post
            category = detect_category(post)

            # The generate_comment function checks for uniquness and stores the post and the comment in a MongoDB database.
            comment = generate_comment(post)

            formdata = {'post': post, 'comment': comment, 'ner':ner_dict, 'category':category}

            # Save the post and the generated comment (REST api purposes)
            entry = postandcomment.objects.create(post=formdata['post'], comment=formdata['comment'])
            entry.save()
        
        else:
            formdata = {'post': None, 'comment': None, 'ner':None, 'category':None}

    return render(request, 'demoapp/generate.html', {'formdata': formdata})


from rest_framework import viewsets
from .serializers import dataSerializer

class pcViewSet(viewsets.ModelViewSet):
   queryset = postandcomment.objects.all()
   serializer_class = dataSerializer
