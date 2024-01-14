from django.urls import path
from .views import *
urlpatterns = [

    path('', BookListView.as_view(), name='booklistview')
]
