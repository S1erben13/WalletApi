from django.urls import path
from api import views

urlpatterns = [

    path('', views.WalletList.as_view()),
    path('<uuid:uuid>/', views.WalletApi.as_view(), name='wallet_detail'),
    path('<uuid:uuid>/operation', views.WalletOperation.as_view(), name='wallet_operation'),

]