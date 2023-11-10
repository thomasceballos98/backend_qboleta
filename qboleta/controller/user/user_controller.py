from prisma import Prisma
from firebase_admin import auth
from flask import abort


async def create_user(decoded_token: str, json_user: dict) -> dict:
    name = json_user.get('name')
    phone = json_user.get('phone')
    country_phone = json_user.get('country_phone')
    document_number = json_user.get('document_number')
    try:
        uid = decoded_token['uid']
        email = decoded_token['email']
        db = Prisma()
        await db.connect()
        # write your queries here
        user = await db.users.create(
            data={
                'id': uid,
                'name': name,
                'email': email,
                'phone': phone,
                'country_phone': country_phone,
                'document_number': document_number
            },
        )
        await db.disconnect()
    except Exception as error:
        abort(409, "User or document already exist ")

    response = {
        'status': True
    }
    return response


async def update_user(decoded_token: str, json_user: dict) -> dict:
    name = json_user.get('name')
    phone = json_user.get('phone')
    country_phone = json_user.get('country_phone')
    document_number = json_user.get('document_number')
    try:
        uid = decoded_token['uid']
        email = decoded_token['email']
        db = Prisma()
        await db.connect()
        # write your queries here
        user = await db.users.update(
            where={
                'id': uid
            },
            data={
                'id': uid,
                'name': name,
                'email': email,
                'phone': phone,
                'country_phone': country_phone,
                'document_number': document_number
            },
        )
        await db.disconnect()
    except Exception as error:
        abort(404, "User doesn't exist ")

    response = {
        'status': True
    }
    return response


async def getInfoToken(decoded_token: str) -> dict:
    try:
        uid = decoded_token['uid']
        db = Prisma()
        await db.connect()
        # write your queries here
        user = await db.users.find_unique(
            where={
                "id": uid
            }
        )
        if not user:
            abort(500, str("No se encontro usuario con el id:" + uid))
    except Exception as error:
        abort(500, str(error))

    response = {
        "uid": uid,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "country_phone": user.country_phone,
        "is_verified": user.is_verified,
        "rating": user.rating,
        "qty_sold": user.qty_sold,
    }
    return response


def verify_auth(token: str) -> dict:
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        email = decoded_token['email']

    except Exception as error:
        abort(500, str(error))
    response = {
        'uid': uid,
        'email': email

    }
    return response
