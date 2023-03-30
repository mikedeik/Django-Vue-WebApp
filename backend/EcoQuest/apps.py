from django.apps import AppConfig



class EcoquestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'EcoQuest'
    #

    def ready(self):
        # import .signals
        import EcoQuest.signals

