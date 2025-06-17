from rest_framework import serializers


class InputSerializer(serializers.Serializer):
    transport = serializers.CharField()             # Transport mode
    departure_country = serializers.CharField()     # ISO code of departure country
    destination_country = serializers.CharField()   # ISO code of destination country
    departure_lat = serializers.FloatField()        # Latitude of departure point
    departure_long = serializers.FloatField()       # Longitude of departure point
    destination_lat = serializers.FloatField()      # Latitude of destination point
    destination_long = serializers.FloatField()     # Longitude of destination point
    year = serializers.CharField()                   # Year for emission factors
    carpooling = serializers.IntegerField(default=1)  # Number of passengers
    is_round_trip = serializers.BooleanField(default=False)  # Is round trip