from datetime import datetime
from django.conf import settings


def date_firma(request):
    return {
        "firma": settings.FIRMA,
        "an_curent": datetime.now().year,
    }