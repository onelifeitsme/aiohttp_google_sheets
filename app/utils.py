import hashlib
import hmac
import json
import os
from app.google_sheets.models import Credentials


def hash_password(password) -> str:
    hashed = hmac.new(
        key=os.environ.get('SECRET_KEY').encode(),
        msg=password.encode(),
        digestmod=hashlib.sha256,
    )
    return hashed.hexdigest()


async def get_credentials_json(user_id):
    credentals_data = await Credentials.query.gino.all()
    credentals_data = credentals_data[0]
    credentals_data = credentals_data.__values__
    credentals_data.pop('id')
    credentals_data.pop('user_id')
    credentals_data = json.dumps(credentals_data, indent=2)
    with open('sample.json', 'w') as f:
        file = f.write(credentals_data)


class Validator:

    def __init__(self, email, password1, password2, credentials=None):
        self.email = email
        self.password1 = password1
        self.password2 = password2
        self.credentials = credentials
        self.invalid_fields_errors = {}

    def is_valid(self):
        try:
            self.validate_password()
        except Exception as password_exception:
            self.invalid_fields_errors['password'] = str(str(password_exception))
        try:
            self.validate_credentals()
        except Exception as credential_exception:
            self.invalid_fields_errors['credentials'] = str(credential_exception)
        if not self.invalid_fields_errors:
            return True
        return False

    def validate_password(self):
        if not self.password1 == self.password2:
            raise Exception('Пароли не совпадают')
        if len(self.password1) < 6:
            raise Exception('Пароль слишком короткий')

    def validate_credentals(self):
        if not isinstance(self.credentials, dict):
            raise Exception('Убедитесь, что прикрепляете верный файл credentals.json')
        if not all([self.credentials.get('type'), self.credentials.get('project_id'), self.credentials.get('private_key_id'),
                   self.credentials.get('private_key'), self.credentials.get('client_email'), self.credentials.get('client_id'),
                   self.credentials.get('auth_uri'), self.credentials.get('token_uri'), self.credentials.get('auth_provider_x509_cert_url'),
                   self.credentials.get('client_x509_cert_url')]):
            raise Exception('Убедитесь, что прикрепляете верный файл credentals.json')








