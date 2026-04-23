from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('', views.ResourceListView.as_view(), name='resource_list'),
    path('resource/<int:pk>/', views.ResourceDetailView.as_view(), name='resource_detail'),
    path('resource/<int:pk>/api/bookings/', views.api_resource_bookings, name='api_resource_bookings'),
    path('booking/<int:pk>/cancel/', views.cancel_booking, name='cancel_booking'),
]
