from django.urls import path
from accounts import views

app_name = "accounts"

urlpatterns = [
    path('login/', views.login_view,name="login"),
    path('signup/', views.signup_view,name="signup"),
    path('profile/', views.profile,name="profile"),
    path('logout/', views.logout_view,name="logout"),
    path('qrcode/', views.qrcode_view,name="qrcode"),
    path('created/', views.created,name="created"),
]