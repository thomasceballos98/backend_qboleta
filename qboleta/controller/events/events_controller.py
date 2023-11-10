from prisma import Prisma
from flask import abort
from firebase_admin import auth
from datetime import datetime
from babel.dates import format_datetime

## Funciones de los maps

def response_get_all_events(x) -> dict:
    a = {
        'id':x.id,
        'name': x.name,
        'created':format_datetime(x.created, "EEE, d MMM y hh:mm", locale='es_ES'),
        'event_date': format_datetime(x.event_date, "EEE, d MMM y hh:mm", locale='es_ES'),
        'user_creator_id': x.user_creator_id,
        'country': x.country,
        'state': x.state,
        'city': x.city,
        'location': x.location,
        'event_type_id': x.event_type_id,
        'event_image': x.event_image
    }
    return a
def response_get_event_types(x) -> dict:
    a = {
        'name': x.name,
        'description': x.description,
        'is_active': x.active,
        'id': x.id
    }
    return a

async def create_event(decoded_token: str, json_event: dict) -> dict:
    name = json_event.get('name')
    event_date = json_event.get('event_date').replace('.000', '')
    event_date_dt = datetime.strptime(event_date, '%Y-%m-%d %H:%M:%S')
    country = json_event.get('country')
    state = json_event.get('state')
    city = json_event.get('city')
    location = json_event.get('location')
    event_type_id = json_event.get('event_type_id')
    event_image = None if not json_event.get('event_image') else json_event.get('event_image')
    try: 
        uid = decoded_token['uid']
        current_date = datetime.now()
        db = Prisma()
        await db.connect()
        # write your queries here
        event = await db.events.create(
            data={
                'name': name,
                'created': current_date,
                'event_date': event_date_dt,
                'user_creator_id': uid,
                'country': country,
                'state': state,
                'city': city,
                'location': location,
                'event_type_id': event_type_id,
                'event_image': event_image
            },
        )

        await db.disconnect()
    except Exception as error:
        abort(500, str(error))

    
    response = {
        'status' :True
    }
    return response


async def get_events_types() -> dict:
    try:
        db = Prisma()
        await db.connect()
        events_types = await db.events_types.find_many(
            where={
                'active': 1,
            },
        )
    except Exception as error:
        abort(500, str(error))

    response = list(map(response_get_event_types, events_types))
    
    return response

async def get_all_events() -> dict:
    try:
        db = Prisma()
        await db.connect()
        events = await db.events.find_many(
            where={
                'active': 1,
            },
        )
    except Exception as error:
        abort(500, str(error))

    response = list(map(response_get_all_events, events))
    return response

async def get_event_by_id(event_id: str) -> dict:
    try:
        db = Prisma()
        await db.connect()
        event = await db.events.find_first(
            where={
                'active': 1,
                'id': int(event_id)
            },
            include={
                'events_type': True
            }
        )
        if not event:
            abort(500, "Do not exist event with id" + event_id)
    except Exception as error:
        abort(500, str(error))

    response = {
        'id':event.id,
        'name': event.name,
        'created':event.created,
        'event_date': event.event_date,
        'user_creator_id': event.user_creator_id,
        'country': event.country,
        'state': event.state,
        'city': event.city,
        'location': event.location,
        'event_type_id': event.event_type_id, 
        'event_image': event.event_image,
        'event_type': event.events_type.name
    }
    return response

async def get_event_by_type_id(type_id: str) -> dict:
    try:
        db = Prisma()
        await db.connect()
        events = await db.events.find_many(
            where={
                'active': 1,
                'event_type_id': int(type_id)
            },
        )
        if not events:
            abort(500, "Do not exist events with type id" + type_id)
    except Exception as error:
        abort(500, str(error))

    response = list(map(response_get_all_events, events))
    return response
