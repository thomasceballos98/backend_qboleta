from flask import Blueprint, request, abort
from jsonschema import validate
from ...functions.schema_management import schema_new_ticket, schema_update_ticket
from ...controller.tickets.tickets_controller import get_tickets_types, create_ticket, update_ticket, get_tickets
from ...middleware.auth import validate_firebase_token


api_tickets = Blueprint("api_tickets", __name__)


@api_tickets.route('/create', methods=['POST'])
@validate_firebase_token
async def createTicket(decoded_token):
    try:
        json_ticket = request.json
        validate(instance=json_ticket, schema=schema_new_ticket)
    except Exception as error:
        error = str(error).split("\n")[0]
        abort(400, ' '.join(["Invalid input data type:", error]))

    response = await create_ticket(decoded_token, json_ticket)
    return response, 200


@api_tickets.route('/update-ticket', methods=['PUT'])
@validate_firebase_token
async def updateTicket(decoded_token):
    try:
        json_ticket = request.json
        validate(instance=json_ticket, schema=schema_update_ticket)
    except Exception as error:
        error = str(error).split("\n")[0]
        abort(400, ' '.join(["Invalid input data type:", error]))

    response = await update_ticket(decoded_token, json_ticket)
    return response, 200


@api_tickets.route('/get-tickets-types', methods=['GET'])
async def getTicketTypes():
    response = await get_tickets_types()
    return response, 200


@api_tickets.route('/get-tickets/<event_id>', methods=['GET'])
async def getTickets(event_id):
    response = await get_tickets(event_id)
    return response, 200
