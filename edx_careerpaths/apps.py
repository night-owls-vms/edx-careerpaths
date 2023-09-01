"""
edx_careerpaths Django application initialization.
"""

from django.apps import AppConfig
from edx_django_utils.plugins.constants import (
    PluginURLs, PluginSettings, PluginContexts, PluginSignals
)


class EdxCareerpathsConfig(AppConfig):
    """
    Configuration for the edx_careerpaths Django application.
    """

    name = 'edx_careerpaths'
    verbose_name = 'Edx CareerPaths'
    # Class attribute that configures and enables this app as a Plugin App.
    plugin_app = {

        # Configuration setting for Plugin URLs for this app.
        PluginURLs.CONFIG: {

            # Configure the Plugin URLs for each project type, as needed. The full list of project types for edx-platform is
            # here:
            # https://github.com/openedx/edx-platform/blob/2dc79bcab42dafed2c122eb808cdd5604327c890/openedx/core/djangoapps/plugins/constants.py#L14 .
            # Other IDAs may use different values.
            'lms.djangoapp': {

                # The namespace to provide to django's urls.include.
                PluginURLs.NAMESPACE: 'edx-careerpaths',

                # The application namespace to provide to django's urls.include.
                # Optional; Defaults to None.
                PluginURLs.APP_NAME: 'careerpaths',

                # The regex to provide to django's urls.url.
                # Optional; Defaults to r''.
                PluginURLs.REGEX: r'^api/edx-careerpaths/',

                # The python path (relative to this app) to the URLs module to be plugged into the project.
                # Optional; Defaults to 'urls'.
                PluginURLs.RELATIVE_PATH: 'api.urls',
            }
        },

        # Configuration setting for Plugin Settings for this app.
        PluginSettings.CONFIG: {

            # Configure the Plugin Settings for each Project Type, as needed. The full list of setting types for edx-platform is
            # here:
            # https://github.com/openedx/edx-platform/blob/2dc79bcab42dafed2c122eb808cdd5604327c890/openedx/core/djangoapps/plugins/constants.py#L25 .
            # Other IDAs may use different values.
            'lms.djangoapp': {

                # Configure each settings, as needed.
                'production': {

                    # The python path (relative to this app) to the settings module for the relevant Project Type and Settings Type.
                    # Optional; Defaults to 'settings'.
                    PluginSettings.RELATIVE_PATH: 'settings.production',
                },
                'common': {
                    PluginSettings.RELATIVE_PATH: 'settings.common',
                },
            }
        },

        # # Configuration setting for Plugin Signals for this app.
        # PluginSignals.CONFIG: {

        #     # Configure the Plugin Signals for each Project Type, as needed.
        #     'lms.djangoapp': {

        #         # The python path (relative to this app) to the Signals module containing this app's Signal receivers.
        #         # Optional; Defaults to 'signals'.
        #         PluginSignals.RELATIVE_PATH: 'my_signals',

        #         # List of all plugin Signal receivers for this app and project type.
        #         PluginSignals.RECEIVERS: [{

        #             # The name of the app's signal receiver function.
        #             PluginSignals.RECEIVER_FUNC_NAME: 'on_signal_x',

        #             # The full path to the module where the signal is defined.
        #             PluginSignals.SIGNAL_PATH: 'full_path_to_signal_x_module.SignalX',

        #             # The value for dispatch_uid to pass to Signal.connect to prevent duplicate signals.
        #             # Optional; Defaults to full path to the signal's receiver function.
        #             PluginSignals.DISPATCH_UID: 'my_app.my_signals.on_signal_x',

        #             # The full path to a sender (if connecting to a specific sender) to be passed to Signal.connect.
        #             # Optional; Defaults to None.
        #             PluginSignals.SENDER_PATH: 'full_path_to_sender_app.ModelZ',
        #         }],
        #     }
        # },

        # # Configuration setting for Plugin Contexts for this app.
        # PluginContexts.CONFIG: {

        #     # Configure the Plugin Signals for each Project Type, as needed.
        #     'lms.djangoapp': {

        #         # Key is the view that the app wishes to add context to and the value
        #         # is the function within the app that will return additional context
        #         # when called with the original context
        #         'course_dashboard': 'my_app.context_api.get_dashboard_context'
        #     }
        # }
    }
