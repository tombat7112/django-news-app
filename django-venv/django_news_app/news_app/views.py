from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView, CreateView
from .models import Post
from pip._vendor import requests
from bs4 import BeautifulSoup
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Post
from .serializers import PostSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


def article_info(url):
# Function to webscrape for info from the url given in the form and the API post request

    result = requests.get(url)
    content = result.content
    soup = BeautifulSoup(content, 'lxml')

    article_title = soup.find('h1').get_text()

    try:
        article_timestamp = soup.find('div', {'class': 'date date--v2'})['data-seconds']
    except:
        article_timestamp = soup.find('time')['data-timestamp']

    article_datetime = datetime.fromtimestamp(int(article_timestamp)).strftime('%Y-%m-%d %H:%M')

    try:
        article_text_paragraphs = soup.find('div', {'class': 'story-body__inner'}).find_all('p')
        article_text = article_text_paragraphs[0].get_text()
    except:
        article_text_paragraphs = soup.find('div', {'class': 'story-body sp-story-body gel-body-copy'}).find_all('p')
        article_text = article_text_paragraphs[0].get_text()
    
    for paragraph in article_text_paragraphs[1:]:
        article_text += ' ' + paragraph.get_text()
    
    return(article_title, article_datetime, article_text)

class PostListView(ListView):
# Paginated view of most recent 10 articles
    model = Post
    template_name = 'news_app/home.html'
    context_object_name = 'posts'
    ordering = ['-date']
    paginate_by = 10

class PostDetailView(DetailView):
# Contains a detailed view of an individual post
    model = Post

class PostCreateView(CreateView):
# Contains the form for the UI post creator
    model = Post
    fields = ['url']

    def form_valid(self, form):

        try:
            form.instance.title, form.instance.date, form.instance.text = article_info(form.instance.url)
            return super().form_valid(form)
        except:
            return HttpResponse(400)

class PostView(APIView):
# Deals with the API requests

    def get(self, request):

        posts = Post.objects.all()

        serializer = PostSerializer(posts, many=True)

        return Response({"Posts": serializer.data})

    def post(self, request):
        
        url = request.data.get('url')

        title, datetime, text = article_info(url)

        data = {
            'url' : url,
            'title' : title,
            'date' : datetime,
            'text' : text
        }

        # Create an article from the above data
        serializer = PostSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            article_saved = serializer.save()
        return Response({"success": "Post '{}' created successfully".format(article_saved.title)})
