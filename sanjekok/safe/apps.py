from django.apps import AppConfig

class SafeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'safe'

    def ready(self):
        # from .tasks import start_scheduler
        # start_scheduler()
        pass # 실행연결 X
