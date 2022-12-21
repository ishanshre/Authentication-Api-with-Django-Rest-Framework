from django.urls import path

from accounts import views

from rest_framework_simplejwt.views import TokenRefreshView
app_name = "accounts"



urlpatterns = [
    path("login/",views.LoginApiView.as_view(), name="login"),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('register/', views.RegisterApiView.as_view(), name="register"),
    path("verify/", views.VerifyEmail.as_view(), name="email_verify"),
    path("resend-verify/", views.ResendEmailLinkApiView.as_view(), name='resend'),
    path("user/", views.UserApiView.as_view(), name="get_user"),
]