from django.contrib.auth.views import LogoutView
from django.forms.formsets import all_valid
from django.urls import path
from django.views.generic.edit import DeleteView

from .views import DeleteUserView, UserLogoutView, all_workouts, index, about, UserLoginView, profile, ChangeUserInfoView, UserPasswordChangeView, RegisterUserView, RegisterDoneView, user_activate, workout


app_name = 'main'
urlpatterns = [
    path('workouts/<int:pk>/', workout, name='workout'),
    path('workouts/', all_workouts, name='workouts'),
    path('accounts/profile/delete/', DeleteUserView.as_view(), name='profile_delete'),
    path('account/register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/password/change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('acoounts/logout/', UserLogoutView.as_view(), name='logout'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/login/', UserLoginView.as_view(), name='login'),
    path('<str:page>/', about, name='about'),
    path('', index, name='index'),
]

