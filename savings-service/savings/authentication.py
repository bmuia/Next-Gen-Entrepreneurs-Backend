import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from decouple import config 

class UserDict(dict):
    """
    A simple proxy class to make the JWT payload behave like a Django User object
    for permission checks.
    """
    def __init__(self, payload):
        super().__init__(payload)
   
        if 'user_id' in self:
            try:
                self['user_id'] = int(self['user_id'])
            except (ValueError, TypeError):
                # Optionally handle this as an AuthenticationFailed exception
                pass

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False


PUBLIC_KEY_CONTENT = config('PUBLIC_KEY')

PUBLIC_KEY = f"""
-----BEGIN PUBLIC KEY-----
{PUBLIC_KEY_CONTENT}
-----END PUBLIC KEY-----
"""

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return None 

        token = auth_header.split(' ')[1]

        try:
            payload = jwt.decode(token, PUBLIC_KEY, algorithms=['RS256'])
        except ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except InvalidTokenError:
            raise AuthenticationFailed('Invalid token')
        except Exception as e:
            # Print the error for debugging
            print(f"Authentication failed during token decoding: {e}")
            raise AuthenticationFailed(f'Authentication failed: {str(e)}')
            
        user = UserDict(payload)
        return (user, token)