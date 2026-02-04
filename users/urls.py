from django.urls import path
from rest_framework.routers import DefaultRouter

from users.views import UserRegistrationView, UserLoginView, UserLogoutView
from users.views.user_self import UserSelfView, ChangePasswordView, UserAvatarUpdateView

router = DefaultRouter()

urlpatterns = [
    #---------- User ----------
    path('user/registration/', UserRegistrationView.as_view(), name='user-registration'),
    path('user/login/', UserLoginView.as_view(), name='user-login'),
    path('user/logout/', UserLogoutView.as_view(), name='user-logout'),

    #---------- User-self ----------
    path('user-self/', UserSelfView.as_view(), name='user-self'),
    path('user-self/change-password/', ChangePasswordView.as_view(), name='change-password'),

#---------- User avatars ----------
    path("user-self/avatar/", UserAvatarUpdateView.as_view(), name="user-avatar"),
]