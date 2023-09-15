"""
URLs for edx_careerpaths.
"""
from django.urls import path, re_path  # pylint: disable=unused-import
from . import views

app_name = 'v1'
urlpatterns = [
    # TODO: Fill in URL patterns and views here.
    # re_path(r'', TemplateView.as_view(template_name="edx_careerpaths/base.html")),
    path('careerpaths', views.CareerPathInfoAPIView.as_view(), name='careerpaths'),
    path('levels', views.LevelAPIView.as_view(), name="levels"),
    path('pathcourses', views.CareerPathCourseAPIView.as_view(), name="Path Courses"),
    path('careerpaths/<int:pk>', views.getcareerpaths)
    # path('home', views.gethomeapi())
]