from django.contrib import admin
from .models import (
    Passenger,
    Flight,
    Reservation
)

admin.site.register(Passenger)
admin.site.register(Flight)
admin.site.register(Reservation)