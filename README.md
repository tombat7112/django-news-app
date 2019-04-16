# django-news-app

To run this application please download all files and install the requirements.txt
This can be installed in the global interpreter or in a virtual environment

After installing the dependencies please run the application by navigating to the following directory:

```
django-venv\django_news_app\news_app
```

and run 

```
python manage.py runserver
```
To view the application use your browser to navigate to  [127.0.0.1:8000](http://127.0.0.1:8000)

To create new article posts make a POST request to [127.0.0.1:8000/api](http://127.0.0.1:8000/api) and pass a url in the body of the request with the key of url
