import platform
import os

from flask import Flask, request, Response, jsonify

app = Flask(__name__)


@app.route("/")
def main():
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
        creds = request.get_json().get("identification")
        if not(creds) or check_auth(creds) is False:
            return Response("Please check auth creds.", 401)

    car_id = creds.get("identification").get("car_id")
    latitude = request.get_json()["location"]["latitude"]
    longitude = request.get_json()["location"]["longitude"]
    location_text = f"Location for {car_id} is {latitude}, {longitude}"
    print(location_text)
    return jsonify(request.get_json())


def check_auth(creds) -> bool:
    """This function is used to authenticate requests.
    """
    username = os.getenv("STREET_SWEEPING_ALERT_USERNAME")
    password = os.getenv("STREET_SWEEPING_ALERT_PASSWORD")
    if creds.get("username") == username and creds.get("password") == password:
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
