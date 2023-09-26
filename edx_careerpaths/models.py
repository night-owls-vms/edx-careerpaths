"""
Database models for edx_careerpaths.
"""
import logging
from django.db import models, IntegrityError

log = logging.getLogger(__name__)

class CareerPathManager(models.Manager):
    def submit_careerpath(self, careerpath_obj):
        try:
            obj, is_created = self.get_or_create(
                name=careerpath_obj["name"],
                description=careerpath_obj["description"]
            )
            log.info("The career path is created")
        except IntegrityError:
            log.info(
                "An IntegrityError was raised when trying to create a new career path for %s:%s", name, description
            )
            obj = self.get(
                name=careerpath_obj["name"],
            )
            is_created = False

        return obj, is_created
    
class LevelManager(models.Manager):
    def submit_level(self, level_obj):
        try:
            obj, is_created = self.get_or_create(
                name=level_obj["name"]
            )
            log.info("New level is created")
        except IntegrityError:
            log.info(
                "An IntegrityError was raised when trying to create a new career path for %s:%s", name, description
            )
            obj = self.get(
                name=level_obj["name"],
            )
            is_created = False

        return obj, is_created
    
class CourseManager(models.Manager):
    def submit_course(self, course_obj):
        try:
            obj, is_created = self.get_or_create(
                id=course_obj["course_id"],
                name=course_obj["name"]
            )
        except IntegrityError:
            log.info(
                "An IntegrityError was raised when trying to create a new career path for %s:%s", course_obj["course_id"], course_obj["name"]
            )
            is_created = False
        return obj, is_created
    
class PathCourseManager(models.Manager):
    def submit_path_course(self, path_course_obj):
        try:
            obj, is_created = self.get_or_create(
                careerpath=CareerPath.objects.get(id=path_course_obj["careerpath_id"]) ,
                course=Course.objects.get(id=path_course_obj["course_id"]),
                level=Level.objects.get(id=path_course_obj["level_id"]) 
            )
        except IntegrityError:
            log.info(
                "An IntegrityError was raised when trying to create a new career path for %s:%s", path_course_obj["careerpath_id"], path_course_obj["course_id"]
            )
            obj = self.get(
                careerpath=path_course_obj["careerpath_id"],
                course_id=path_course_obj["course_id"],
                level=path_course_obj["level_id"]
            )
            is_created = False

        return obj, is_created

class CareerPath(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25, null=False)
    description = models.TextField()

    objects = CareerPathManager()

    def __str__(self) -> str:
        return f"{self.id} {self.name}"

    @property
    def get_name(self):
        return "%s"%(str(self.name))
    
    @property
    def courses_count(self):
        return PathCourse.objects.filter(careerpath=self.id).count()

    
class Level(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25, null=False, unique=True)
    # order = models.SmallIntegerField(unique=True, null=False)

    objects = LevelManager()

    def __str__(self) -> str:
        return self.name
    
    @property
    def get_name(self):
        return "%s"%(str(self.name))
    
class Course(models.Model):
    id = models.CharField(max_length=250, primary_key=True)
    name = models.CharField(max_length=150, null=False)

    objects = CourseManager()

    def __str__(self) -> str:
        return self.name

class PathCourse(models.Model):
    id = models.AutoField(primary_key=True)
    careerpath = models.ForeignKey(CareerPath, on_delete=models.CASCADE, null=False)
    course = models.ForeignKey(Course, null=False, blank=False, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=False)
    # course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)

    objects = PathCourseManager()
    
    def __str__(self) -> str:
        return f"{self.id} {self.course_id} {self.careerpath.name} {self.level.name}"
    
    @property
    def level_name(self):
        return self.level.name
    
    @property
    def career_path_name(self):
        return self.careerpath.name
    
    @property
    def course_name(self):
        return self.course.name
    
