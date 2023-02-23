from django.urls import path
from django.conf.urls import url, include

from . import views

app_name = 'users'

urlpatterns = [
    path('', views.profile, name='profile'),
    url(r'^verified-email-field/', include('verified_email_field.urls')),
    # path('signup/', SignUpView.as_view(), name='signup'),
]
# urlpatterns = [
#     path('signup/', SignUpView.as_view(), name='signup'),
# ]
