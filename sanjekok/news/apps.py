from django.apps import AppConfig

class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'
    
    def ready(self):
        from sanjekok.scheduler import start_scheduler
        start_scheduler()
        
        # pass # 실행 안할려면 pass
