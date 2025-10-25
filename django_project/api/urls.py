from django.urls import path
from .views import PredictPriceAPIView, house_form,home

urlpatterns = [
    path('', home, name='home'),
    path('predict/', PredictPriceAPIView.as_view(), name='predict-price'),
    path('form/', house_form, name='house-form'),
]
