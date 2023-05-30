from rest_framework import serializers
from .models import (
    Passenger,
    Flight,
    Reservation
)


# -----------------------------------------------------------
# --------------------- FixSerializer -----------------------
# -----------------------------------------------------------
class FixSerializer(serializers.ModelSerializer):

    created = serializers.StringRelatedField()
    created_id = serializers.IntegerField(required=False)

    def create(self, validated_data):
        validated_data['created_id'] = self.context['request'].user.id
        return super().create(validated_data)


# -----------------------------------------------------------
# --------------------- PassengerSerializer -----------------
# -----------------------------------------------------------
class PassengerSerializer(FixSerializer):

    gender_text = serializers.SerializerMethodField()

    class Meta:
        model = Passenger
        exclude = []

    def get_gender_text(self, obj):
        return obj.get_gender_display()


# -----------------------------------------------------------
# --------------------- FlightSerializer --------------------
# -----------------------------------------------------------
class FlightSerializer(FixSerializer):

    departure_text = serializers.SerializerMethodField() # return from get_field_name()
    arrival_text = serializers.SerializerMethodField()

    class Meta:
        model = Flight
        fields = (
            "id",
            "created",
            "created_id",
            "departure_text",
            "arrival_text",
            "created_time",
            "updated_time",
            "flight_number",
            "airline",
            "departure",
            "departure_date",
            "arrival",
            "arrival_date",
            "get_airline_display", # dont need SerializerMethodField.
        )

    # SerializerMethodField()
    def get_departure_text(self, obj):
        return obj.get_departure_display()
    
    # SerializerMethodField
    def get_arrival_text(self, obj):
        return obj.get_arrival_display()


# -----------------------------------------------------------
# --------------------- ReservationSerializer ---------------
# -----------------------------------------------------------
class ReservationSerializer(FixSerializer):
    
    flight_id = serializers.IntegerField(write_only=True)
    passenger_ids = serializers.ListField(write_only=True)

    flight = FlightSerializer(read_only=True) # ForeingKey()
    passenger = PassengerSerializer(read_only=True, many=True) # ManyToMany()

    class Meta:
        model = Reservation
        exclude = []

    def create(self, validated_data):
        validated_data["passenger"] = validated_data.pop('passenger_ids')
        return super().create(validated_data)