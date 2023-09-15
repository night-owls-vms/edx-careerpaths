# import json
# from attr import asdict
# import logging

# from .utils import serialize_course_key, masked_dict, PluginJSONEncoder

# log = logging.getLogger(__name__)
# log.info("openedx_plugins.signals loaded")

# def certificate_created(certificate, **kwargs):
#     """
#     see apps.py plugin_app["signals_config"]["lms.djangoapp"]["receivers"]
#     signal_path: openedx_events.learning.signals.COURSE_UNENROLLMENT_COMPLETED
#     https://github.com/openedx/openedx-events/blob/main/openedx_events/learning/signals.py#L85

#     event_type: org.openedx.learning.certificate.created.v1
#     event_name: CERTIFICATE_CREATED
#     event_description: emitted when the user's certificate creation process is completed.
#     event_data: CertificateData
#     """

#     certificate_info = asdict(
#         certificate,
#         value_serializer=serialize_course_key,
#     )
#     event_metadata = asdict(kwargs.get("metadata"))
#     payload = {
#         "certificate": certificate_info,
#         "event_metadata": event_metadata,
#     }

#     log.info(
#         "openedx_plugin received CERTIFICATE_CREATED signal for {payload}".format(
#             payload=json.dumps(masked_dict(payload), cls=PluginJSONEncoder, indent=4)
#         ))