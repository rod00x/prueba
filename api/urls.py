from django.urls import path
from .views import *

app_name = 'api'

urlpatterns = [
    path('products/', Product_APIView.as_view()),
    path('inventories/product/<int:pk>/', Product_APIView_Detail.as_view()),
    path('orders/<int:pk>/', Product_APIView_Detail.as_view())
]
