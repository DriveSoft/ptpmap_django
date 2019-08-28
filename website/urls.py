from django.urls import include, path
from .views import HomePage

urlpatterns = [
    path('', HomePage.as_view(), name='homepage'),
]
