from rest_framework.test import APIRequestFactory, APITestCase
from django.contrib.auth.models import User, AnonymousUser
from .models import Passenger, Flight, Reservation
from .views import FlightView
from rest_framework.test import force_authenticate
from rest_framework.authtoken.models import Token
from django.urls import reverse



class ModelsTestCase(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        # self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user = User.objects.create_user(
            username='tarik',
            email='tarik@gmail.com',
            password='Canpo$#1536'
        )
        # self.token = Token.objects.get(user=self.user)

        # self.token = Token.objects.create(user=self.user)

        # print(self.token.key)
        
        self.passenger = Passenger.objects.create(
            created=self.user,
            first_name='John',
            last_name='Doe',
            email='johndoe@example.com',
            gender='M'
        )
      
        self.flight = Flight.objects.create(
            created=self.user,
            flight_number='ABC123',
            airline='THY',
            departure=1,
            departure_date='2023-05-26',
            arrival=6,
            arrival_date='2023-05-26'
        )
        self.reservation = Reservation.objects.create(created=self.user, flight=self.flight)
        self.reservation.passenger.add(self.passenger)

    def test_passenger_str(self):
        passenger = Passenger.objects.get(first_name='John', last_name='Doe')
        self.assertEqual(str(passenger), 'John Doe')

    def test_flight_str(self):
        flight = Flight.objects.get(flight_number='ABC123')
        self.assertEqual(str(flight), 'ABC123 # THY')

    def test_reservation_str(self):
        reservation = Reservation.objects.get(flight=self.flight)
        self.assertEqual(str(reservation), 'ABC123 # THY [1]')

    def test_reservation_passenger_count(self):
        reservation = Reservation.objects.get(flight=self.flight)
        self.assertEqual(reservation.passenger.count(), 1)

    def test_reservation_passenger(self):
        reservation = Reservation.objects.get(flight=self.flight)
        passenger = reservation.passenger.first()
        self.assertEqual(passenger.first_name, 'John')
        self.assertEqual(passenger.last_name, 'Doe')

    def test_reservation_flight(self):
        reservation = Reservation.objects.get(flight=self.flight)
        flight = reservation.flight
        self.assertEqual(flight.flight_number, 'ABC123')
        self.assertEqual(flight.airline, 'THY')

    def test_flight_list_as_guest_user(self):
        request = self.factory.get(reverse('flight-list'))
        request.user = AnonymousUser()
        response = FlightView.as_view({'get':'list'})(request)
        self.assertEqual(response.status_code, 200)

    def test_flight_create_as_guest_user(self):
        request = self.factory.post(reverse('flight-list'))
        request.user = AnonymousUser()
        response = FlightView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 401)
          
    def test_flight_create_as_admin_user(self):
        data = {
            "flight_number": "TK100",
            "airline": "THY",
            "departure": 7,
            "arrival": 6,
            "departure_date": "2023-05-26",
            "arrival_date": "2023-05-26"
        }
        request = self.factory.post(reverse('flight-list'), data, format='json')
        force_authenticate(request, user=self.user)
        self.user.is_staff = True
        self.user.save()
        response = FlightView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 201)
        
    def test_flight_update_as_admin_user(self):
        data = {
            "flight_number": "TK100",
            "airline": "THY",
            "departure": 6,
            "arrival": 1,
            "departure_date": "2023-05-26",
            "arrival_date": "2023-05-26"
        }
        url = reverse('flight-detail', kwargs={'pk': 1})
        request = self.factory.put(url, data, format='json')
        force_authenticate(request, user=self.user)
        self.user.is_staff = True
        self.user.save()
        response = FlightView.as_view({'put': 'update'})(request, pk='1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Flight.objects.get(id=1).flight_number, 'TK100')
        self.assertEqual(Flight.objects.count(), 1)
    
    def test_flight_delete_as_admin_user(self):
        url = reverse('flight-detail', kwargs={'pk': 1})
        request = self.factory.delete(url)
        force_authenticate(request, user=self.user)
        self.user.is_staff = True
        self.user.save()
        response = FlightView.as_view({'delete': 'destroy'})(request, pk='1')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Flight.objects.count(), 0)
        # In this code, we are creating a DELETE request to the flight detail endpoint (flight-detail), targeting the flight with pk=1. We then authenticate the request as an admin user using force_authenticate and proceed with the deletion. Finally, we assert that the response status code is 204 (indicating successful deletion) and check that the flight object has been removed from the database (Flight.objects.count() should be 0).#
        
    # def test_flight_create_as_login_user(self):
    #     request = self.factory.post(reverse('flight-list'), HTTP_AUTHORIZATION='Token ' + self.token.key)
    #     # force_authenticate(request, user=self.user)
    #     response = FlightView.as_view({'post': 'create'})(request)
    #     self.assertEqual(response.status_code, 403)