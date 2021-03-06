from sanic_jwt import initialize

from app import create_app
from app.users.auth import authenticate, retrieve_user, extend_payload, store_refresh_token, retrieve_refresh_token

app = create_app()
initialize(app, url_prefix='/token', authenticate=authenticate, retrieve_user=retrieve_user, extend_payload=extend_payload,
           refresh_token_enabled=True, store_refresh_token=store_refresh_token,
           retrieve_refresh_token=retrieve_refresh_token)

if __name__ == "__main__":
    HOST, PORT, DEBUG = app.config['HOST'], app.config['PORT'], app.config['DEBUG']
    app.run(host=HOST, port=PORT, debug=DEBUG)
