from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'apps.users'
    
    # register signals
    # This ensures signals are loaded when Django starts.
    def ready(self):
        import apps.users.signals
