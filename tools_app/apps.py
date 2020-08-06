import logging
import sys
from django.apps import AppConfig


logger = logging.getLogger('tools_app.apps')


class ToolsAppConfig(AppConfig):
    name = 'tools_app'

    def ready(self):
        if 'manage.py' not in sys.argv[0]:
            logger.critical(f'{self.name} starting (argv = {sys.argv})')
