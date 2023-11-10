# Users schemas

schema_new_user = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "phone": {"type": "string"},
        "country_phone": {"type": "string"},
        "document_number": {"type": "string"},
    },
    "required": ["name", "phone", "country_phone", "document_number"]
}

# Events schemas
schema_new_event = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "event_date": {"type": "string", "format": "date"},
        "country": {"type": "string"},
        "state": {"type": "string"},
        "city": {"type": "string"},
        "location": {"type": "string"},
        "event_type_id": {"type": "number"},
        "event_image": {"type": "string"}
    },
    "required": ["name", "event_date", "country", "state", "city", "location", "event_type_id"]
}

# Tickets schemas
schema_new_ticket = {
    "type": "object",
    "properties": {
        "ticket_type_id": {"type": "number"},
        "event_id": {"type": "number"},
        "tickets_qty": {"type": "number"},
        "price": {"type": "number"},
        "description": {"type": "string"}
    },
    "required": ["ticket_type_id", "event_id", "tickets_qty", "price", "description"]
}
# Tickets schemas
schema_update_ticket = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "ticket_type_id": {"type": "number"},
        "event_id": {"type": "number"},
        "tickets_qty": {"type": "number"},
        "price": {"type": "number"},
        "description": {"type": "string"}
    },
    "required": ["id", "ticket_type_id", "event_id", "tickets_qty", "price", "description"]
}
