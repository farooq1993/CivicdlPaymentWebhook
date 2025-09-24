def extract_event_fields(payload: dict):
    """
    Normalize payload -> (event_type, event_id, payment_id, amount, currency)
    """
    event_type = payload.get("event") or payload.get("event_type")
    event_id = payload.get("id") or payload.get("event_id")

    # Razorpay style
    entity = payload.get("payload", {}).get("payment", {}).get("entity", {})
    payment_id = entity.get("id") or payload.get("payment_id")
    amount = entity.get("amount") or payload.get("amount")
    currency = entity.get("currency") or payload.get("currency")

    return event_type, event_id, payment_id, amount, currency
