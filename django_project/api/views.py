from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import joblib
import numpy as np
from .serializers import PredictPriceSerializer

# بارگذاری مدل‌ها و LabelEncoder
xgb_model = joblib.load("house_price_xgb_final.joblib")
scaler = joblib.load("scaler.joblib")
address_encoder = joblib.load("address_encoder.joblib")

# ----------- API برای POST JSON -----------
class PredictPriceAPIView(APIView):
    def post(self, request):
        serializer = PredictPriceSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            address_num = address_encoder.transform([data['Address']])[0]

            X = np.array([[
                data['Area'],
                data['Room'],
                int(data['Parking']),
                int(data['Warehouse']),
                int(data['Elevator']),
                address_num
            ]])
            X_scaled = scaler.transform(X)
            prediction = xgb_model.predict(X_scaled)[0]

            # تبدیل به عدد با جداکننده هزارگان
            formatted_prediction = f"{int(prediction):,}"

            return Response({"predicted_price": formatted_prediction}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------- HTML Form -----------
import pandas as pd

model = xgb_model  # مدل پیش‌بینی برای فرم
le_address = address_encoder  # LabelEncoder برای فرم

def house_form(request):
    prediction = None
    if request.method == "POST":
        address = request.POST.get("address")
        area = float(request.POST.get("area"))
        bedrooms = int(request.POST.get("rooms"))
        parking = int(request.POST.get("parking"))
        warehouse = int(request.POST.get("warehouse"))
        elevator = int(request.POST.get("elevator"))

        # تبدیل آدرس به عدد
        address_encoded = le_address.transform([address])[0]

        # آماده‌سازی دیتا برای پیش‌بینی
        X = np.array([[area, bedrooms, parking, warehouse, elevator, address_encoded]])
        X_scaled = scaler.transform(X)
        pred = model.predict(X_scaled)[0]

        # فرمت عدد برای نمایش خوانا
        prediction = f"{int(pred):,}"

    return render(request, "house_form.html", {"prediction": prediction})
