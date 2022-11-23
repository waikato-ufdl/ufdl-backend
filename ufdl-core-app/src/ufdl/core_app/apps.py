from django.apps import AppConfig


class UFDLCoreAppConfig(AppConfig):
    name = 'ufdl.core_app'
    label = "ufdl_core"

    def ready(self):
        # @receiver decorator takes care of registration of signals
        from . import signals
