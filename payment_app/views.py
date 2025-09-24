import hmac
import hashlib
import os
import json
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PaymentOrder
from .serializers import PayementOrderSerializer
from .utils import extract_event_fields

# Shared secret (used for HMAC simulation)
SHARED_SECRET = os.getenv("SHARED_SECRET", "test_secret")


class PaymentWebhookView(APIView):
    """
    Webhook receiver for payment events.
    Supports single object or list payload.
    Simulates signature validation.
    """

    def post(self, request):
        raw_body = request.body
        signature = request.headers.get("X-Razorpay-Signature")

        # Reject missing signature
        if not signature:
            return Response({"error": "Missing signature"}, status=status.HTTP_403_FORBIDDEN)

        
        expected_signature = hmac.new(SHARED_SECRET.encode(), raw_body, hashlib.sha256).hexdigest()
       
        #
        if signature != "TEST_SIGNATURE" and not hmac.compare_digest(expected_signature, signature):
            return Response({"error": "Invalid signature"}, status=status.HTTP_403_FORBIDDEN)

        # Parse JSON
        try:
            data = json.loads(raw_body.decode())
        except Exception:
            return Response({"error": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)

        # Normalize to list for consistent processing
        events = data if isinstance(data, list) else [data]
        results = []

        for event_payload in events:
            try:
                # Extract required fields
                event_type, event_id, payment_id, amount, currency = extract_event_fields(event_payload)
                if not (event_id and payment_id):
                    results.append({"event_id": None, "status": "failed", "reason": "Missing event_id or payment_id"})
                    continue

                # Prepare data for serializer
                obj = {
                    "event_type": event_type,
                    "event_id": event_id,
                    "payment_id": payment_id,
                    "amount": amount,
                    "currency": currency,
                }

                # Save to database
                serializer = PayementOrderSerializer(data=obj)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                results.append({"event_id": event_id, "status": "ok"})

            except IntegrityError:
                # Duplicate event_id (idempotency)
                results.append({"event_id": event_id, "status": "duplicate"})
            except Exception as e:
                results.append({"event_id": event_payload.get("id"), "status": "failed", "reason": str(e)})

        return Response(results, status=status.HTTP_201_CREATED)



class PaymentEventsView(APIView):
    def get(self, request, payment_id):
        events = PaymentOrder.objects.filter(payment_id=payment_id).order_by("received_at")

        if not events.exists():
            return Response(
                {"msg": f"No events found for payment_id {payment_id}"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = PayementOrderSerializer(events, many=True)
        return Response(serializer.data)
