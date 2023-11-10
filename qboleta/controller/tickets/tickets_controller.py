from prisma import Prisma
from flask import abort
from firebase_admin import auth


def response_get_ticket_types(x) -> dict:
    a = {
        'id': x.id,
        'description': x.description,
        'is_active': x.active,
        'name': x.name
    }
    return a


def response_get_tickets(x) -> dict:
    a = {
        'ticket_type_id': x.ticket_type_id,
        'price': x.price,
        'tickets_qty': x.tickets_qty,
        'description': x.description,
        'id': x.id,
        'events_id': x.event_id,
        'selling': x.users.name,
        'country_phone': x.users.country_phone,
        'phone': x.users.phone,
        'tickets_sold': x.users.qty_sold,
        'rating': x.users.rating,
        'ticket_type': x.ticket_type.name
    }
    return a


async def create_ticket(decoded_token: str, json_event: dict) -> dict:
    ticket_type_id = json_event.get('ticket_type_id')
    event_id = json_event.get('event_id')
    tickets_qty = json_event.get('tickets_qty')
    price = json_event.get('price')
    description = json_event.get('description')

    try:
        uid = decoded_token['uid']
        db = Prisma()
        await db.connect()
        # write your queries here
        ticket = await db.tickets.create(
            data={
                'ticket_type_id': ticket_type_id,
                'user_owner_id': uid,
                'event_id': event_id,
                'tickets_qty': tickets_qty,
                'price': price,
                'description': description,
            },
        )

        await db.disconnect()
    except Exception as error:
        abort(500, str(error))

    response = {
        'status': True
    }
    return response


async def update_ticket(decoded_token: str, json_event: dict) -> dict:
    id = json_event.get('id')
    ticket_type_id = json_event.get('ticket_type_id')
    event_id = json_event.get('event_id')
    tickets_qty = json_event.get('tickets_qty')
    price = json_event.get('price')
    description = json_event.get('description')

    uid = decoded_token['uid']
    db = Prisma()
    await db.connect()

    ticket = await db.tickets.find_first(
        where={
            'id': id,
            'user_owner_id': uid
        }
    )

    if ticket is None:
        abort(403, "This user is not the owner of this ticket")

    try:

        # write your queries here
        ticket = await db.tickets.update(
            where={
                'id': id,
            },
            data={
                'ticket_type_id': ticket_type_id,
                'user_owner_id': uid,
                'event_id': event_id,
                'tickets_qty': tickets_qty,
                'price': price,
                'description': description,
            },
        )

        await db.disconnect()
    except Exception as error:
        abort(403, "Error updating ticket")

    response = {
        'status': True
    }
    return response


async def get_tickets_types() -> dict:
    try:
        db = Prisma()
        await db.connect()
        ticket_types = await db.tickets_types.find_many(
            where={
                'active': 1,
            },
        )
    except Exception as error:
        abort(500, str(error))

    response = list(map(response_get_ticket_types, ticket_types))

    return response


async def get_tickets(event_id) -> dict:
    event_id = int(event_id)
    try:
        db = Prisma()
        await db.connect()
        tickets = await db.tickets.find_many(
            where={
                'active': 1,
                'event_id': event_id
            },
            include={
                "users": True,
                "ticket_type": True
            }
        )
    except Exception as error:
        abort(500, str(error))

    response = list(map(response_get_tickets, tickets))

    return response
