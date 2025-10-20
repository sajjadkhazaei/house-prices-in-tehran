from rest_framework import serializers

class HouseDataSerializer(serializers.Serializer):
    Area = serializers.FloatField()
    Room = serializers.FloatField()
    Parking = serializers.FloatField()
    Warehouse = serializers.FloatField()
    Elevator = serializers.FloatField()
    '''price_per_meter = serializers.FloatField()'''
    Address_by_number= serializers.FloatField()
    
'''from rest_framework import serializers
from .models import House_predict

# Serializer for Task model
class House_predict_Serializer(serializers.ModelSerializer):
    class Meta:
        model = House_predict
        fields = '__all__'
----
from rest_framework import serializers
from django.db import models

class House_predict(models.Model) :
    Area = models.IntegerField(blank=False)
    Room = models.IntegerField()
    Parking = models.IntegerField(max_length=10)
    Warehouse = models.IntegerField(max_length=10)
    Elevator = models.IntegerField(max_length=10)
    Address_by_number = models.FloatField(default=False)

    def __str__(self):
        return self.Area'''
