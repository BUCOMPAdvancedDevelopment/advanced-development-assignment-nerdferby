from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "tsml_users"

    def ready(self):
        import tsml_users.signals
