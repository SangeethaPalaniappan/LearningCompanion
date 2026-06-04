from django.contrib.auth import views as auth_views
from django.urls import path
from .forms import EmailOrUsernameAuthenticationForm
from .views import GetDetails, SignUpView

urlpatterns = [
    #path("<str:day>", GetDetails.as_view(), name="get")
    path("", GetDetails.as_view(), name="get"),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(authentication_form=EmailOrUsernameAuthenticationForm),
        name="login",
    ),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("accounts/signup/", SignUpView.as_view(), name="signup"),
]
