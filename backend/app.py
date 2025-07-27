from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from functools import wraps
from models import db, User, Quiz, Score, Subject, Chapter
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
CORS(app)
jwt = JWTManager(app)

# --- A more robust admin decorator ---
def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if current_user.get('role') != 'admin':
            return jsonify(msg="Admins only!"), 403
        return fn(*args, **kwargs)
    return wrapper

# --- Auth APIs ---
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('fullName')
    
    if User.query.filter_by(username=email).first():
        return jsonify({"msg": "User with this email already exists"}), 409

    new_user = User(
        username=email,
        full_name=full_name,
        qualification=data.get('qualification')
    )
    new_user.set_password(password)
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"msg": "User registered successfully"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(username=email).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity={'id': user.id, 'role': user.role})
        return jsonify(access_token=access_token)
    
    return jsonify({"msg": "Bad username or password"}), 401

# --- Subject Management APIs ---
@app.route('/api/subjects', methods=['GET'])
@admin_required
def get_all_subjects():
    subjects = Subject.query.order_by(Subject.name).all()
    return jsonify([{'id': s.id, 'name': s.name, 'description': s.description} for s in subjects])

@app.route('/api/subjects', methods=['POST'])
@admin_required
def create_subject():
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({"msg": "Missing subject name"}), 400
    
    if Subject.query.filter_by(name=data['name']).first():
        return jsonify({"msg": "A subject with this name already exists"}), 409
    
    new_subject = Subject(name=data['name'], description=data.get('description', ''))
    db.session.add(new_subject)
    db.session.commit()
    
    return jsonify({'id': new_subject.id, 'name': new_subject.name, 'description': new_subject.description}), 201

@app.route('/api/subjects/<int:subject_id>', methods=['PUT'])
@admin_required
def update_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    data = request.get_json()
    
    subject.name = data.get('name', subject.name)
    subject.description = data.get('description', subject.description)
    db.session.commit()
    
    return jsonify({'id': subject.id, 'name': subject.name, 'description': subject.description})

@app.route('/api/subjects/<int:subject_id>', methods=['DELETE'])
@admin_required
def delete_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    db.session.delete(subject)
    db.session.commit()
    return jsonify({"msg": "Subject deleted successfully"}), 200

# --- User Dashboard APIs ---
@app.route('/api/user/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    identity = get_jwt_identity()
    user_id = identity['id']
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    return jsonify({"fullName": user.full_name})

@app.route('/api/quizzes', methods=['GET'])
@jwt_required()
def get_available_quizzes():
    quizzes = Quiz.query.all()
    quiz_list = [
        {
            "id": quiz.id,
            "title": f"Quiz for Chapter {quiz.chapter_id}",
            "description": quiz.remarks or f"Duration: {quiz.time_duration}"
        } for quiz in quizzes
    ]
    return jsonify(quiz_list)

@app.route('/api/user/scores', methods=['GET'])
@jwt_required()
def get_user_scores():
    identity = get_jwt_identity()
    user_id = identity['id']
    scores = Score.query.filter_by(user_id=user_id).order_by(Score.time_stamp.desc()).all()
    score_list = [
        {
            "id": score.id,
            "quizName": f"Quiz #{score.quiz_id}",
            "score": score.total_scored,
            "date": score.time_stamp.strftime('%Y-%m-%d')
        } for score in scores
    ]
    return jsonify(score_list)

# --- App Runner ---
if __name__ == '__main__':
    with app.app_context():
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