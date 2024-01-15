from django.urls import path
from .views import *
urlpatterns = [

    path('book/', BookListView.as_view(), name='booklistview'),
    path('books/', BookListCreateViewApi.as_view()),
    path('booksupper/<int:pk>',BookDeleteUpdateViewApi.as_view()),
    path('book/detail/<int:pk>/', BookDetailApi.as_view()),
     path('book/delete/<int:pk>/', BookDeleteApi.as_view()),
     path('book/update/<int:pk>/', BookUpdateApi.as_view()),
    path('bookdef/', book_view),
    path('book/create/', BookCreateView.as_view())
]
