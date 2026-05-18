from django.urls import path
from .views import GetDetails

urlpatterns = [
    #path("<str:day>", GetDetails.as_view(), name="get")
    path("", GetDetails.as_view(), name="get")
]