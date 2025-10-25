from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import joblib
import numpy as np
import pandas as pd
from .serializers import PredictPriceSerializer
import os
from django.conf import settings

# load joblib files
BASE_DIR = settings.BASE_DIR  
MODEL_PATH = os.path.join(BASE_DIR, "house_price_xgb_final.joblib")
SCALER_PATH = os.path.join(BASE_DIR, "scaler.joblib")
ENCODER_PATH = os.path.join(BASE_DIR, "address_encoder.joblib")

xgb_model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
address_encoder = joblib.load(ENCODER_PATH)

most_common_address_encoded = 0  # default
try:
    classes = list(address_encoder.classes_)
except Exception:
    pass

class PredictPriceAPIView(APIView):
    def post(self, request):
        serializer = PredictPriceSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            # encode address
            address_text = str(data['Address'])
            if address_text in list(address_encoder.classes_):
                address_num = int(address_encoder.transform([address_text])[0])
            else:
                address_num = int(most_common_address_encoded)

            # prepare input as DataFrame with column names
            X = pd.DataFrame([[
                data['Area'],
                data['Room'],
                int(data['Parking']),
                int(data['Warehouse']),
                int(data['Elevator']),
                address_num,
                data['price_per_meter']
            ]], columns=['Area','Room','Parking','Warehouse','Elevator','Address','price_per_meter'])

            # scale & predict
            X_scaled = scaler.transform(X)
            pred = xgb_model.predict(X_scaled)[0]

            pred = max(pred, 0)

            formatted = f"{int(round(pred)):,}"
            return Response({"predicted_price": formatted}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------- HTML Form view ----------
def house_form(request):
    prediction = None
    error = None
    negative_input_warning = None  

    if request.method == "POST":
        try:
            address = request.POST.get('address', '')
            area = float(request.POST.get('area', 0))
            rooms = int(request.POST.get('rooms', 0))
            parking = int(request.POST.get('parking', 0))
            warehouse = int(request.POST.get('warehouse', 0))
            elevator = int(request.POST.get('elevator', 0))
            price_per_meter = float(request.POST.get('price_per_meter', 0))

            if address in list(address_encoder.classes_):
                address_num = int(address_encoder.transform([address])[0])
            else:
                address_num = int(most_common_address_encoded)

            X = pd.DataFrame([[area, rooms, parking, warehouse, elevator, address_num, price_per_meter]],
                             columns=['Area','Room','Parking','Warehouse','Elevator','Address','price_per_meter'])
            X_scaled = scaler.transform(X)
            pred = xgb_model.predict(X_scaled)[0]

            if pred < 0:
                prediction = None
                negative_input_warning = "The inputs are unrealistic, the prediction was negative. Please adjust the inputs."
            else:
                prediction = f"{int(round(pred)):,}"
        except Exception as e:
            error = str(e)

    address_choices = list(address_encoder.classes_)

    return render(request, "house_form.html", {
        "prediction": prediction,
        "error": error,
        "negative_input_warning": negative_input_warning,
        "address_choices": address_choices
    })
    
    
def home(request):
    return render(request, 'home.html')
