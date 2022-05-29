import platform
import base64
import os

from flask import Flask, request, Response

app = Flask(__name__)


@app.route("/")
def hello_world():
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    os_type = platform.system()
    if os_type == "Linux":
        client_auth = request.headers.get('CSOAUTH')
        if not(client_auth) or check_auth(client_auth) is False:
            return Response("Please check auth creds.", 401)

    request_json = request.get_json()
    if request.args and "message" in request.args:
        return request.args.get("message")
    elif request_json and "message" in request_json:
        return request_json["message"]
    else:
        return "Hello World!"


def check_auth(client_auth) -> bool:
    """This function is used to authenticate requests.
    When creating a new service (Cloud Functions or Cloud Run),
    remember to generate a password (GUID) and save the credentials in Google Secret Manager.

    GUID's can be generated using this code:
    import uuid
    str(uuid.uuid4())

    The name of the Cloud Secret should be formatted as f"CSOAUTH_{SERVICE_NAME}".
    Secret names should be all caps and unserscores in place of spaces and dashes.
    Example: If the name of this service "random-etl-service",
    the authentication password should be saved as: "CSOAUTH_RANDOM_ETL_SERVICE".

    This makes it easy to predect secret names if you know
    the service name and have accesss to Secret Manager.
    """
    CSOAUTH = os.getenv(f"CSOAUTH_{os.getenv('K_SERVICE').upper().replace('-', '_')}")
    if CSOAUTH == client_auth:
        return True
    else:
        return False


if __name__ == "__main__":
    """Checks operating system.
    If Windows, it runs the app in dev/debug mode.
    If Linux, it runs in production mode.
    """
    os_type = platform.system()
    if os_type == "Windows":
        app.run(debug=True, host="localhost", port=8080)
    elif os_type == "Linux":
        app.run(debug=False, host="0.0.0.0", port=8080)
