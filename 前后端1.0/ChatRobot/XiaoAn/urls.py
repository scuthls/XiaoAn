#urls.py
from django.conf.urls import url
from . import views

urlpatterns = [
     url(r'^xiaoan/',views.TestView.as_view()),
 ]