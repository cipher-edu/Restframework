from django.urls import path
from .views import *
urlpatterns = [
    # path('<int:pk>/', PostDetail.as_view() ),
    path("", PostList.as_view())
]
