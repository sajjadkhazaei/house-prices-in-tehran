from rest_framework import serializers

class PredictPriceSerializer(serializers.Serializer):
    Area = serializers.FloatField()
    Room = serializers.IntegerField()
    Parking = serializers.IntegerField()
    Warehouse = serializers.IntegerField()
    Elevator = serializers.IntegerField()
    Address = serializers.CharField()
