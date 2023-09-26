# python stuff
import os
import json
import requests
import logging

# django stuff
from django.contrib.auth import get_user_model
from django.http.response import HttpResponseNotFound
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError

from rest_framework.decorators import api_view
from rest_framework import status, permissions
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
# open edx stuff
from opaque_keys.edx.keys import CourseKey

from edx_rest_framework_extensions.auth.jwt.authentication import JwtAuthentication
from edx_rest_framework_extensions.auth.session.authentication import SessionAuthenticationAllowInactiveUser
# our stuff
from edx_careerpaths.models import (
    CareerPath,
    Level,
    PathCourse,
    Course,
)
from edx_careerpaths.api.v1.utils import get_course_image

log = logging.getLogger(__name__)

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']

class isAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if (request.method in SAFE_METHODS or request.user and request.user.is_superuser):
            return True
        return False

class ResponseSuccess(Response):
    def __init__(self, data=None, http_status=None, content_type=None):
        _status = http_status or status.HTTP_200_OK
        data = data or {}
        reply = {"response": {"success": True}}
        reply["response"].update(data)
        super().__init__(data=reply, status=_status, content_type=content_type)

class CareerPathInfoAPIView(APIView):
    authentication_classes = (
        JwtAuthentication, SessionAuthenticationAllowInactiveUser
    )
    permission_classes = (isAuthenticatedOrReadOnly,)
    REQUIRED_KEYS = ['name', 'description']

    def _validate(self, careerpath_object):
        """
        Perform validation
        """
        for key in self.REQUIRED_KEYS:
            if key not in careerpath_object:
                raise ValidationError(_("Key '{key}' not found.").format(key=key))
        
        return careerpath_object

    def get(self, request, pk=None):
        response = {}
        careerpath_id = request.query_params.get('id')
        if careerpath_id:
            try:
                careerpath = CareerPath.objects.get(id=careerpath_id)
                response["name"] = careerpath.name
                response["description"] = careerpath.description
                pathcourses = PathCourse.objects.filter(careerpath_id=careerpath_id)
                levels = []
                courses = {}
                for course in pathcourses:
                    result_course = {}
                    result_course["id"] = course.id
                    key = CourseKey.from_string(course.course_id)
                    course_image = get_course_image(key)
                    id = course.course_id.split(":")[1]
                    result_course["image_url"] = f"asset-v1:{id}+type@asset+block@{course_image}"
                    result_course["course_id"] = course.course_id
                    result_course["name"] = course.course_name
                    result_course["level_name"] = course.level_name
                    if course.level_name not in courses:
                        courses[course.level_name] = [result_course]
                    else:
                        courses[course.level_name].append(result_course)

                for key, value in courses.items():
                    level_orders = {
                        "Beginner": 1,
                        "Intermediate": 2,
                        "Advanced": 3
                    }
                    level_dict = {
                        "level": key,
                        "level_order": level_orders[key],
                        "courses": value
                    }
                    levels.append(level_dict)
                sorted_levels = sorted(levels, key=lambda x: x['level_order'])
                response["level_courses"] = sorted_levels
            except CareerPath.DoesNotExist:
                response["error"] = "This career path not found."
            finally:
                return Response(response, status=status.HTTP_200_OK)
        
        careerpaths = CareerPath.objects.all()
        results = [{"id": careerpath.id, "name": careerpath.name, "description":careerpath.description, "courses_count": careerpath.courses_count} for careerpath in careerpaths]
        response["careerpaths"] = results
        return Response(response)
    
    def post(self, request, *args, **kwargs):
        """
        Create a new careerpath
        """
        careerpath_object = request.data
        print(careerpath_object)
        try:
            careerpath_object = self._validate(careerpath_object)
            CareerPath.objects.submit_careerpath(careerpath_object)
        except ValidationError as exc:
            return Response({
                "detail": _(' ').join(str(msg) for msg in exc.messages),
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": _("{name} career path created successfully.".format(name=careerpath_object["name"]))},status=status.HTTP_201_CREATED)
    
    def delete(self, request):
        careerpath_id = request.query_params.get('id')
        response = {}
        try:
            instance = CareerPath.objects.get(id=careerpath_id)
            instance.delete()
            response["detail"] = _("{name} career path deleted successfully.").format(name = instance.name)
        except CareerPath.DoesNotExist:
            return Response({
                "error": _("Career path {careerpath_id} do not exists.").format(careerpath_id=careerpath_id),
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response(response, status=status.HTTP_200_OK)
    
class LevelAPIView(APIView):
    authentication_classes = (
        JwtAuthentication, SessionAuthenticationAllowInactiveUser
    )
    permission_classes = (permissions.IsAdminUser,)
    REQUIRED_KEYS = ['name']

    def _validate(self, level_object):
        """
        Perform validation
        """
        for key in self.REQUIRED_KEYS:
            if key not in level_object:
                raise ValidationError(_("Key '{key}' not found.").format(key=key))
        
        return level_object

    def get(self, request):
        response = {}
        levels = Level.objects.all()
        levels = [{"id": level.id, "name": level.name} for level in levels]
        sorted_levels = sorted(levels, key=lambda x: x['id'])
        response["levels"] = sorted_levels
        return Response(response)
    
    def post(self, request):
        level_object = request.data
        try:
            level = self._validate(level_object)
            Level.objects.submit_level(level)
        except ValidationError as exc:
            return Response({
                "detail": _(' ').join(str(msg) for msg in exc.messages),
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": _("{name} level created successfully.".format(name=level_object["name"]))},status=status.HTTP_201_CREATED)

class CareerPathCourseAPIView(APIView):
    authentication_classes = (
        JwtAuthentication, SessionAuthenticationAllowInactiveUser
    )
    permission_classes = (isAuthenticatedOrReadOnly,)
    REQUIRED_KEYS = ['course_id', 'careerpath_id', 'level_id']

    def _validate(self, path_course_object):
        """
        Perform validation
        """
        for key in self.REQUIRED_KEYS:
            if key not in path_course_object:
                print(
                    _("Key '{key}' not found.").format(key=key)
                )
                raise ValidationError(_("Key '{key}' not found.").format(key=key))
            
        try:
            Course.objects.get(id=path_course_object["course_id"])
        except Course.DoesNotExist:
            log.info("Course not found.")
            url = "http://localhost:18000/api/courses/v1/courses/" + path_course_object["course_id"] + "/"
            response = requests.get(url)
            course_info = response.json()
            print(course_info)
            course_obj = {
                "course_id": path_course_object["course_id"],
                "name": course_info["name"]
            }
            Course.objects.submit_course(course_obj=course_obj)
        return path_course_object

    def get(self, request):
        response = {}
        path_course_id = request.query_params.get('id')
        path_id = request.query_params.get('path_id')

        if path_course_id:
            try:
                pathcourse = PathCourse.objects.get(id=path_course_id)
                response["id"] = pathcourse.id
                response["course_id"] = pathcourse.course_id
                response["career_path_name"] = pathcourse.career_path_name
                response["level_name"] = pathcourse.level_name
            except PathCourse.DoesNotExist:
                response["error"] = "This career path not found."
            finally:
                return Response(response, status=status.HTTP_200_OK)
            
        if path_id:
            try:
                careerpath = CareerPath.objects.get(id=path_id)
                response["name"] = careerpath.name
                response["description"] = careerpath.description
                pathcourses = PathCourse.objects.filter(careerpath_id=path_id)
                courses = []
                for course in pathcourses:
                    result_course = {}
                    result_course["id"] = course.id
                    result_course["course_id"] = course.course_id
                    result_course["course_name"] = course.course_name
                    result_course["level_name"] = course.level_name
                    courses.append(result_course)
                response["courses"] = courses
            except PathCourse.DoesNotExist:
                response["error"] = "This career path not found."
            finally:
                return Response(response, status=status.HTTP_200_OK)
        response["info"] = "Career Path Id parameter required."
        return Response(response, status=status.HTTP_200_OK)
            
    def post(self, request, *args, **kwargs):
        """
        Create new path course
        """
        path_course_object = request.data
        try:
            path_course_object = self._validate(path_course_object)
            PathCourse.objects.submit_path_course(path_course_object)
        except ValidationError as exc:
            return Response({
                "detail": _(' ').join(str(msg) for msg in exc.messages),
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Create Action successful."},status=status.HTTP_201_CREATED)
    
    def delete(self, request):
        path_course_id = request.query_params.get('id')
        response = {}
        try:
            instance = PathCourse.objects.get(id=path_course_id)
            instance.delete()
            response["detail"] = _("Delete Action Success.")
        except CareerPath.DoesNotExist:
            return Response({
                "error": _("Path Course {path_course_id} do not exists.").format(path_course_id=path_course_id),
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response(response, status=status.HTTP_200_OK)

@api_view(["GET"])
def getcareerpaths(request, pk):
    if request.method == "GET":
        if pk:
            result = {}
            careerpath_info = CareerPath.objects.get(id=pk)
            result["name"] = careerpath_info.name
            result["description"] = careerpath_info.description
            pathcourses = PathCourse.objects.filter(careerpath_id=pk)
            courses = {}
            for course in pathcourses:
                result_course = {}
                result_course["id"] = course.id
                key = CourseKey.from_string(course.course_id)
                course_image = get_course_image(key)
                id = course.course_id.split(":")[1]
                result_course["image_url"] = f"asset-v1:{id}+type@asset+block@{course_image}"
                result_course["course_id"] = course.course_id
                result_course["course_name"] = course.course_name
                result_course["level_name"] = course.level_name
                if course.level_name not in courses:
                    courses[course.level_name] = [result_course]
                else:
                    courses[course.level_name].append(result_course)
                    
            result["courses"] = courses
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Please choose a career path id."}, status=status.HTTP_200_OK)
    return Response({"message": "You are in right track."})