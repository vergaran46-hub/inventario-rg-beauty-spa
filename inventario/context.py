from django.conf import settings


def opciones(request):
    return {'registro_abierto': settings.REGISTRO_ABIERTO}
