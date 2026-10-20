from django.contrib import admin
from .models import Gen, Studio, Distribuitor, Magazin, Raion, Eveniment, Film

admin.site.register([Gen, Studio, Distribuitor, Magazin, Raion, Eveniment, Film])