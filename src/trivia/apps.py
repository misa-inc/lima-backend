from django.apps import AppConfig


class TriviaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'trivia'

    def ready(self):
        import trivia.signals