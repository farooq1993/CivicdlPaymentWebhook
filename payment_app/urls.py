from django.urls import path
from . import views

urlpatterns = [
    path("webhook/payments", views.PaymentWebhookView.as_view(), name="payment-webhook"),
    path("payments/<str:payment_id>/events", views.PaymentEventsView.as_view(), name="payment-events"),
]
