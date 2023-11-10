from flask import Blueprint, request, abort
from jsonschema import validate
from ...functions.schema_management import schema_new_event
from ...controller.events.events_controller import get_events_types, create_event, get_all_events, get_event_by_id, get_event_by_type_id
from ...middleware.auth import validate_firebase_token

api_events = Blueprint("api_events", __name__)

@api_events.route('/create', methods=['POST'])
@validate_firebase_token
async def createEvent(decoded_token):

    try: 
        json_event = request.json
        validate(instance=json_event, schema=schema_new_event)
    except Exception as error:
        error = str(error).split("\n")[0]
        abort(400, ' '.join(["Invalid input data type:", error]))

    response = await create_event(decoded_token, json_event)
    return response, 200

@api_events.route('/get-events-types', methods=['GET'])
async def getEventsTypes():
    response = await get_events_types()
    return response, 200

@api_events.route('/get-all-events', methods=['GET'])
async def getAllEvents():
    response = await get_all_events()
    return response, 200

@api_events.route('/get-event-by-id/<event_id>', methods=['GET'])
async def getEventById(event_id):
    response = await get_event_by_id(event_id)
    return response, 200

@api_events.route('/get-event-by-type-id/<type_id>', methods=['GET'])
async def getEventByTypeId(type_id):
    response = await get_event_by_type_id(type_id)
    return response, 200

