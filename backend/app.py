from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import db, User
from config import Config
# from tasks import make_celery # We'll use this later

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
CORS(app) # Allow requests from your Vue frontend
jwt = JWTManager(app)
# celery = make_celery(app) # We'll use this later

# --- API Endpoints ---

@app.route('/api/register', methods=['POST'])
def register():
    # Get data from the request
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('fullName')
    
    # Check if user already exists
    if User.query.filter_by(username=email).first():
        return jsonify({"msg": "User with this email already exists"}), 409

    # Create new user
    new_user = User(
        username=email,
        full_name=full_name,
        qualification=data.get('qualification'),
        # dob=data.get('dob') # Handle date conversion if needed
    )
    new_user.set_password(password) # Hash the password
    
    # Add to database
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"msg": "User registered successfully"}), 201


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Find user by email
    user = User.query.filter_by(username=email).first()

    # Check if user exists and password is correct
    if user and user.check_password(password):
        # Create JWT token
        access_token = create_access_token(identity={'id': user.id, 'role': user.role})
        return jsonify(access_token=access_token)
    
    return jsonify({"msg": "Bad username or password"}), 401


# Example: Protected Admin Route (for future use)
@app.route('/api/admin/subjects', methods=['POST'])
@jwt_required()
def create_subject():
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({"msg": "Admins only!"}), 403
    # ... (logic to create a subject) ...
    pass


# This block runs the app
if __name__ == '__main__':
    with app.app_context():
        # This command creates the admin user and DB tables if they don't exist
        db.create_all()
        if not User.query.filter_by(username=app.config['ADMIN_EMAIL']).first():
            admin = User(
                username=app.config['ADMIN_EMAIL'],
                full_name='Admin',
                role='admin'
            )
            admin.set_password(app.config['ADMIN_PASSWORD'])
            db.session.add(admin)
            db.session.commit()
            print('Initialized the database and created admin user.')
    
    app.run(debug=True)