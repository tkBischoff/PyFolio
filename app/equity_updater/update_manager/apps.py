from django.apps import AppConfig


class UpdateManagerConfig(AppConfig):
    name = 'update_manager'

    def ready(self):
        from update_manager.update_equitys import updater
        updater.start()
