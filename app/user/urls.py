from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from user import views

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    # path('token/', views.CreateTokenView.as_view(), name='token'),
    # path('get-token/', views.GetTokenView.as_view(), name='get-token'),
    #these are new and we dont need to get-token or token APIs
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('user/', views.UserView.as_view(), name='user'), #alternative to me url
    path('logout/', views.LogoutView.as_view(), name='logout'),


]