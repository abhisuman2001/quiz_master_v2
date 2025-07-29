from flask import Flask, jsonify
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity

# --- Minimal App Setup ---
app = Flask(__name__)
# Use a simple, hardcoded secret key
app.config["JWT_SECRET_KEY"] = "this-is-a-test" 
jwt = JWTManager(app)

# --- Test Routes ---
# This route gives you a token
@app.route("/test-login", methods=["POST"])
def test_login():
    # A hardcoded user identity
    identity = {"id": 1, "role": "admin"}
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)

# This route is protected. It should work if the token is valid.
@app.route("/test-protected", methods=["GET"])
@jwt_required()
def test_protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

if __name__ == "__main__":
    app.run(port=5001) # Running on a different port (5001) to avoid conflicts