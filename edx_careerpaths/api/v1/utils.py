# coding=utf-8
"""
written by:     Lawrence McDaniel
                https://lawrencemcdaniel.com

date:           sep-2021

usage:          utility and convenience functions for
                openedx_plugin_api plugin
"""
# python stuff
from datetime import datetime
from pytz import UTC
import re
import logging

# django stuff
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

# open edx stuff
from opaque_keys.edx.keys import CourseKey
# from common.djangoapps.util.date_utils import get_default_time_display

try:
    # for olive and later
    from xmodule.modulestore.django import (
        modulestore,
    )  # lint-amnesty, pylint: disable=wrong-import-order
except ImportError:
    # for backward compatibility with nutmeg and earlier
    from common.lib.xmodule.xmodule.modulestore.django import (
        modulestore,
    )  # lint-amnesty, pylint: disable=wrong-import-order

log = logging.getLogger(__name__)

def get_course_image(course_key: CourseKey):
    """
    Generate a verbose json object of course
    descriptive and meta data.

    editorial comment: you can create a course key in
    Django shell as follows:
    ----------------
    from opaque_keys.edx.keys import CourseKey
    course_key_str = "course-v1:edX+DemoX+Demo_Course"
    course_key = CourseKey.from_string(course_key_str)

    """
    # store = modulestore()

    with modulestore().bulk_operations(course_key):
        course_module = modulestore().get_course(course_key, depth=0)

    return course_module.course_image
