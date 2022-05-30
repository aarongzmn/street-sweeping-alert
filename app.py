import platform
import os

from flask import Flask, request

app = Flask(__name__)


@app.route("/", methods=["POST"])
def main():
    """Process location data and save vehicle location.
    """
    resp = {
        "data": None,
        "errors": []
    }
    if request.method == "POST":
        if request.authorization is None or check_auth(request.authorization) is False:
            resp["errors"] = "Please check auth creds."
            return resp, 401
        else:
            if request.get_json():
                request_json = request.get_json()
                if "carId" in request_json:
                    if "latitude" in request_json["location"] and "longitude" in request_json["location"]:
                        car_id = request_json["carId"]
                        latitude = request_json["location"]["latitude"]
                        longitude = request_json["location"]["longitude"]
                        location_text = f"Location for {car_id} is {latitude}, {longitude}"
                        print(location_text)
                        resp["data"] = location_text
                        return resp, 200
                    else:
                        resp["errors"] = "Both 'latitude' and 'latitude' are required."
                else:
                    resp["errors"] = "No 'carId' found."
            else:
                resp["errors"] = "No JSON data found."
            return resp, 400


def check_auth(client_auth) -> bool:
    """This function is used to authenticate requests.
    """
    client_user = client_auth.username
    client_pass = client_auth.password

    if platform.system() == "Linux":
        server_user = os.getenv("STREET_SWEEPING_ALERT_USERNAME")
        server_pass = os.getenv("STREET_SWEEPING_ALERT_PASSWORD")
    else:
        server_user = "username"
        server_pass = "password"

    if server_user == client_user and server_pass == client_pass:
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
