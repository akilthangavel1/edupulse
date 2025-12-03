from django.apps import AppConfig


class XstudentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'xstudent'
    
    def ready(self):
        """Import signals when the app is ready"""
        import xstudent.signals