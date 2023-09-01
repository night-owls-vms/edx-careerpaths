"""
Api URLs.
"""

from django.conf.urls import include
from django.urls import path

app_name = 'edx_careerpaths'  # pylint: disable=invalid-name
urlpatterns = [
    path('v1/', include('edx_careerpaths.api.v1.urls')),
]
