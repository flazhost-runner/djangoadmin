from apps.setting.models import Setting


class HomeService:
    def get_landing_data(self) -> dict:
        setting = Setting.objects.first()
        return {'setting': setting}
