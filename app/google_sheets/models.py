from app.store.database.models import db


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_superuser = db.Column(db.Boolean, default=False)


class Credentials(db.Model):
    __tablename__ = "credentials"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    project_id = db.Column(db.String(50), nullable=False)
    private_key_id = db.Column(db.String(120), nullable=False)
    private_key = db.Column(db.Text, nullable=False)
    client_email = db.Column(db.String(120), nullable=False)
    client_id = db.Column(db.String(120), nullable=False)
    auth_uri = db.Column(db.String(120), nullable=False)
    token_uri = db.Column(db.String(120), nullable=False)
    auth_provider_x509_cert_url = db.Column(db.String(120), nullable=False)
    client_x509_cert_url = db.Column(db.String(200), nullable=False)
