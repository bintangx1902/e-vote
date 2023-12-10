from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('candidate', ShowCandidateEndPoint.as_view(), name='candidate'),
    path('vote', vote_candidate_endpoint, name='vote'),
    path('register', UserRegistrationEndPoint.as_view(), name='register'),
    # path('login', UserLoginEndPoint.as_view(), name='login'),
    path('login', obtain_auth_token, name='login'),
    path('logout', logout_view, name='logout'),
]