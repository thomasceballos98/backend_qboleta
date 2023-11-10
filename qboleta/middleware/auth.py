from functools import wraps
from flask import request, jsonify
from firebase_admin import auth

def validate_firebase_token(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        token = token.split()[1]
        if not token:
            return jsonify({"error": "No token provided"}), 403
        
        try:
            # Verificar y decodificar el token
            decoded_token = auth.verify_id_token(token)
            request.user = decoded_token
        except Exception as e:
            return jsonify({"error": f"Invalid token: {str(e)}"}), 403
        
        # Retorna la función f y el token decodificado
        return await f(decoded_token, *args, **kwargs)
    
    return wrapper