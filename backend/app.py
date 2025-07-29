from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from functools import wraps
from models import db, User, Quiz, Score, Subject, Chapter, Question
from config import Config
from tasks import celery, generate_user_performance_report
from flask import send_from_directory
from app_factory import create_app

# --- App Initialization ---
app = create_app()


# --- THIS IS THE FIX: Explicitly configure Celery ---
celery.conf.broker_url = app.config['CELERY_BROKER_URL']
celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']

# ---------------------------------------------------

# --- Custom Decorators ---
def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if user and user.role == 'admin':
            return fn(*args, **kwargs)
        return jsonify(msg="Admins only!"), 403
    return wrapper

# --- Auth APIs ---
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data.get('email')).first():
        return jsonify({"msg": "User with this email already exists"}), 409
    
    new_user = User(
        username=data.get('email'), 
        full_name=data.get('fullName'), 
        qualification=data.get('qualification')
    )
    new_user.set_password(data.get('password'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "User registered successfully"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get('email')).first()
    if user and user.check_password(data.get('password')):
        access_token = create_access_token(identity=user.id, additional_claims={'role': user.role})
        return jsonify(access_token=access_token)
    return jsonify({"msg": "Bad username or password"}), 401

@app.route('/api/admin/stats', methods=['GET'])
@admin_required
def get_admin_stats():
    # Fetch the admin's name
    admin_user_id = get_jwt_identity()
    admin = User.query.get(admin_user_id)
    admin_name = admin.full_name if admin else "Admin"

    # Calculate the counts
    total_subjects = Subject.query.count()
    total_quizzes = Quiz.query.count()
    total_users = User.query.filter(User.role != 'admin').count()
    
    return jsonify({
        "admin_name": admin_name,
        "total_subjects": total_subjects,
        "total_quizzes": total_quizzes,
        "total_users": total_users
    })

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

# --- Chapter Management APIs ---
@app.route('/api/chapters/<int:chapter_id>', methods=['GET'])
@admin_required
def get_chapter_details(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    return jsonify({'id': chapter.id, 'name': chapter.name, 'description': chapter.description})

@app.route('/api/subjects/<int:subject_id>/chapters', methods=['GET'])
@admin_required
def get_chapters_for_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    chapters = [{'id': c.id, 'name': c.name, 'description': c.description} for c in subject.chapters]
    return jsonify(chapters)

@app.route('/api/subjects/<int:subject_id>/chapters', methods=['POST'])
@admin_required
def create_chapter_for_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({"msg": "Missing chapter name"}), 400
    new_chapter = Chapter(name=data['name'], description=data.get('description', ''), subject_id=subject.id)
    db.session.add(new_chapter)
    db.session.commit()
    return jsonify({'id': new_chapter.id, 'name': new_chapter.name, 'description': new_chapter.description}), 201

@app.route('/api/chapters/<int:chapter_id>', methods=['PUT'])
@admin_required
def update_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    data = request.get_json()
    chapter.name = data.get('name', chapter.name)
    chapter.description = data.get('description', chapter.description)
    db.session.commit()
    return jsonify({'id': chapter.id, 'name': chapter.name, 'description': chapter.description})

@app.route('/api/chapters/<int:chapter_id>', methods=['DELETE'])
@admin_required
def delete_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    db.session.delete(chapter)
    db.session.commit()
    return jsonify({"msg": "Chapter deleted successfully"})

# --- Quiz Management APIs ---
@app.route('/api/chapters/<int:chapter_id>/quizzes', methods=['GET'])
@admin_required
def get_quizzes_for_chapter(chapter_id):
    Chapter.query.get_or_404(chapter_id)
    quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
    return jsonify([{'id': q.id, 'time_duration': q.time_duration, 'remarks': q.remarks} for q in quizzes])

@app.route('/api/chapters/<int:chapter_id>/quizzes', methods=['POST'])
@admin_required
def create_quiz_for_chapter(chapter_id):
    Chapter.query.get_or_404(chapter_id)
    data = request.get_json()
    if not data or not data.get('time_duration'):
        return jsonify({"msg": "Missing time duration"}), 400
    new_quiz = Quiz(chapter_id=chapter_id, time_duration=data['time_duration'], remarks=data.get('remarks', ''))
    db.session.add(new_quiz)
    db.session.commit()
    return jsonify({'id': new_quiz.id, 'time_duration': new_quiz.time_duration, 'remarks': new_quiz.remarks}), 201

@app.route('/api/quizzes/<int:quiz_id>', methods=['PUT'])
@admin_required
def update_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    data = request.get_json()
    quiz.time_duration = data.get('time_duration', quiz.time_duration)
    quiz.remarks = data.get('remarks', quiz.remarks)
    db.session.commit()
    return jsonify({'id': quiz.id, 'time_duration': quiz.time_duration, 'remarks': quiz.remarks})

@app.route('/api/quizzes/<int:quiz_id>', methods=['DELETE'])
@admin_required
def delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    db.session.delete(quiz)
    db.session.commit()
    return jsonify({"msg": "Quiz deleted successfully"})

# --- Question Management APIs ---
@app.route('/api/quizzes/<int:quiz_id>/questions', methods=['GET'])
@admin_required
def get_questions_for_quiz(quiz_id):
    Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    return jsonify([{
        'id': q.id, 'statement': q.statement, 'option1': q.option1,
        'option2': q.option2, 'option3': q.option3, 'option4': q.option4,
        'correct_option': q.correct_option
    } for q in questions])

@app.route('/api/quizzes/<int:quiz_id>/questions', methods=['POST'])
@admin_required
def create_question_for_quiz(quiz_id):
    Quiz.query.get_or_404(quiz_id)
    data = request.get_json()
    required_fields = ['statement', 'option1', 'option2', 'option3', 'option4', 'correct_option']
    if not all(field in data for field in required_fields):
        return jsonify({"msg": "Missing required fields for question"}), 400

    new_question = Question(
        quiz_id=quiz_id,
        statement=data['statement'],
        option1=data['option1'],
        option2=data['option2'],
        option3=data['option3'],
        option4=data['option4'],
        correct_option=data['correct_option']
    )
    db.session.add(new_question)
    db.session.commit()
    return jsonify({'id': new_question.id}), 201

@app.route('/api/questions/<int:question_id>', methods=['PUT'])
@admin_required
def update_question(question_id):
    question = Question.query.get_or_404(question_id)
    data = request.get_json()
    question.statement = data.get('statement', question.statement)
    question.option1 = data.get('option1', question.option1)
    question.option2 = data.get('option2', question.option2)
    question.option3 = data.get('option3', question.option3)
    question.option4 = data.get('option4', question.option4)
    question.correct_option = data.get('correct_option', question.correct_option)
    db.session.commit()
    return jsonify({'id': question.id})

@app.route('/api/questions/<int:question_id>', methods=['DELETE'])
@admin_required
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    return jsonify({"msg": "Question deleted successfully"})

# --- User Management APIs (for Admin) ---

@app.route('/api/users', methods=['GET'])
@admin_required
def get_all_users():
    # Fetch all users except the admin to prevent self-modification
    users = User.query.filter(User.role != 'admin').order_by(User.full_name).all()
    return jsonify([{
        'id': u.id,
        'full_name': u.full_name,
        'username': u.username, # email
        'qualification': u.qualification,
        'role': u.role
    } for u in users])

@app.route('/api/users/<int:user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    # Fields an admin is allowed to change
    user.full_name = data.get('full_name', user.full_name)
    user.qualification = data.get('qualification', user.qualification)
    user.role = data.get('role', user.role) # e.g., promote a user to admin
    
    db.session.commit()
    return jsonify({'id': user.id, 'full_name': user.full_name, 'role': user.role})

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == 'admin':
        return jsonify({"msg": "Cannot delete an admin account."}), 403
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg": "User deleted successfully"})


# --- Report Generation API ---
@app.route('/api/admin/reports/user-performance', methods=['POST'])
@admin_required
def trigger_user_report():
    task = generate_user_performance_report.delay()
    return jsonify({"task_id": task.id}), 202 # 202 Accepted

@app.route('/api/admin/reports/status/<task_id>', methods=['GET'])
@admin_required
def get_report_status(task_id):
    task = celery.AsyncResult(task_id)
    response = {
        'state': task.state,
        'result': task.result if task.state == 'SUCCESS' else None
    }
    return jsonify(response)

@app.route('/api/admin/reports/download/<filename>', methods=['GET'])
@admin_required
def download_report(filename):
    return send_from_directory('exports', filename, as_attachment=True)

# --- User Dashboard APIs ---
@app.route('/api/user/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify({"fullName": user.full_name})

@app.route('/api/quizzes', methods=['GET'])
@jwt_required()
def get_available_quizzes():
    quizzes = Quiz.query.all()
    return jsonify([{"id": q.id, "title": f"Quiz for Chapter {q.chapter_id}", "description": q.remarks} for q in quizzes])

@app.route('/api/user/scores', methods=['GET'])
@jwt_required()
def get_user_scores():
    user_id = get_jwt_identity()
    scores = Score.query.filter_by(user_id=user_id).all()
    return jsonify([{"id": s.id, "quizName": f"Quiz #{s.quiz_id}", "score": s.total_scored, "date": s.time_stamp.strftime('%Y-%m-%d')} for s in scores])

# --- Quiz Taking APIs ---

@app.route('/api/quizzes/<int:quiz_id>/attempt', methods=['GET'])
@jwt_required()
def get_quiz_for_attempt(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = quiz.questions
    
    # Return questions without the correct answer
    question_list = [{
        'id': q.id,
        'statement': q.statement,
        'option1': q.option1,
        'option2': q.option2,
        'option3': q.option3,
        'option4': q.option4
    } for q in questions]
    
    return jsonify({
        'quiz_id': quiz.id,
        'time_duration': quiz.time_duration,
        'questions': question_list
    })

@app.route('/api/quizzes/<int:quiz_id>/submit', methods=['POST'])
@jwt_required()
def submit_quiz_attempt(quiz_id):
    data = request.get_json()
    user_answers = data.get('answers') # e.g., {"question_id": "selected_option_num"}
    user_id = get_jwt_identity()
    
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = quiz.questions
    
    score = 0
    total_questions = len(questions)
    
    # Calculate score
    for question in questions:
        # User answers are sent as strings, so convert question.id to string for lookup
        user_answer = user_answers.get(str(question.id))
        if user_answer and int(user_answer) == question.correct_option:
            score += 1
            
    # Save the score to the database
    new_score = Score(
        quiz_id=quiz_id,
        user_id=user_id,
        total_scored=score
    )
    db.session.add(new_score)
    db.session.commit()
    
    return jsonify({
        'msg': 'Quiz submitted successfully!',
        'score': score,
        'total': total_questions
    })

# --- App Runner ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username=app.config['ADMIN_EMAIL']).first():
            admin = User(username=app.config['ADMIN_EMAIL'], full_name='Admin', role='admin')
            admin.set_password(app.config['ADMIN_PASSWORD'])
            db.session.add(admin)
            db.session.commit()
            print('Initialized the database and created admin user.')
    app.run(debug=True, use_reloader=False)