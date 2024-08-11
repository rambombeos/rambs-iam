from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('test-token/', test_token, name='test_token'),
    # path('api_test_post/', api_test_post, name='api_test_post'),  # Added trailing slash
]