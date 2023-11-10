import os
from flask import Blueprint, request, abort, jsonify
from jsonschema import validate
from ...controller.user.user_controller import create_user, update_user, getInfoToken
from ...functions.schema_management import schema_new_user
from ...middleware.auth import validate_firebase_token
api_user = Blueprint("api_user", __name__)


@api_user.route('/index', methods=['GET'])
def index():
    return os.environ.get('THOMAS'), 200


@api_user.route('/create', methods=['POST'])
@validate_firebase_token
async def createUser(decoded_token):
    try:
        json_user = request.json
        validate(instance=json_user, schema=schema_new_user)
    except Exception as error:
        error = str(error).split("\n")[0]
        return jsonify({"error": f"Invalid schema: {str(error)}"}), 403

    response = await create_user(decoded_token, json_user)
    return response, 200


@api_user.route('/update-user', methods=['PUT'])
@validate_firebase_token
async def updateUser(decoded_token):
    try:
        json_user = request.json
        validate(instance=json_user, schema=schema_new_user)
    except Exception as error:
        error = str(error).split("\n")[0]
        return jsonify({"error": f"Invalid schema: {str(error)}"}), 403

    response = await update_user(decoded_token, json_user)
    return response, 200


@api_user.route('/get-user-info', methods=['GET'])
@validate_firebase_token
async def getToken(decoded_token):
    response = await getInfoToken(decoded_token)
    return response, 200

# @api_user.errorhandler(500)
# def handle_internal_server_error(e):
#     return jsonify(error=e.description), 500, {"Content-Type": "application/json"}
