from django.db import models
from django.contrib.auth.models import User


# -----------------------------------------------------------
# --------------------- FixModel ----------------------------
# -----------------------------------------------------------
class FixModel(models.Model):
    created = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True # dont create table.


# -----------------------------------------------------------
# --------------------- Passenger ---------------------------
# -----------------------------------------------------------
class Passenger(FixModel):

    GENDERS = (
        ('F', 'Female'),
        ('M', 'Male'),
        ('0', 'Prefer Not To Say'),
    )

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField()
    gender = models.CharField(max_length=1, choices=GENDERS, default='0')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


# -----------------------------------------------------------
# --------------------- Flight ------------------------------
# -----------------------------------------------------------
class Flight(FixModel):

    AIRLINES = (
        ('THY', 'Turkish Airlines'),
        ('SUN', 'Sun Airlines'),
        ('SEL', 'Selim Airlines'),
    )

    CITIES = (
        (1, 'Adana'),
        (6, 'Ankara'),
        (7, 'Antalya'),
        (9, 'Aydın'),
        (10, 'Balıkesir'),
        (16, 'Bursa'),
        (32, 'Isparta'),
        (34, 'Istanbul'),
        (35, 'Izmir'),
        (44, 'Malatya'),
        (52, 'Ordu'),
    )

    flight_number = models.CharField(max_length=64)
    airline = models.CharField(max_length=3, choices=AIRLINES)
    departure = models.PositiveSmallIntegerField(choices=CITIES)
    departure_date = models.DateField()
    arrival = models.PositiveSmallIntegerField(choices=CITIES)
    arrival_date = models.DateField()

    def __str__(self):
        return f'{self.flight_number} # {self.airline}'


# -----------------------------------------------------------
# --------------------- Reservation -------------------------
# -----------------------------------------------------------
class Reservation(FixModel):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    passenger = models.ManyToManyField(Passenger)

    def __str__(self):
        return f'{self.flight} [{self.passenger.count()}]'