from flask_mail import Mail, Message
import requests
from datetime import datetime, timedelta
from models import db, User, Quiz, Score
from sqlalchemy import and_, func
import jinja2
import os

mail = Mail()

def send_email(to, subject, template_name, **kwargs):
    """Send an email using a template"""
    template_loader = jinja2.FileSystemLoader('templates')
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template(f'{template_name}.html')
    html = template.render(**kwargs)
    
    msg = Message(
        subject,
        recipients=[to],
        html=html
    )
    mail.send(msg)

def send_gchat_message(webhook_url, message):
    """Send a message to Google Chat"""
    try:
        response = requests.post(
            webhook_url,
            json={"text": message}
        )
        return response.status_code == 200
    except:
        return False

def send_daily_reminders():
    """Send daily reminders to users about new quizzes or inactivity"""
    # Get users who haven't taken a quiz in the last 7 days
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    
    inactive_users = User.query.join(
        Score, and_(Score.user_id == User.id, Score.time_stamp > seven_days_ago),
        isouter=True
    ).filter(
        Score.id.is_(None),
        User.role != 'admin',
        User.notification_time <= datetime.utcnow().time()
    ).all()

    # Get new quizzes created in the last 24 hours
    new_quizzes = Quiz.query.filter(
        Quiz.created_at >= datetime.utcnow() - timedelta(days=1)
    ).all()

    for user in inactive_users:
        # Skip if user has disabled notifications
        if not user.notifications_enabled:
            continue

        message = f"Hi {user.full_name},\n\n"
        
        if new_quizzes:
            message += "New quizzes are available:\n"
            for quiz in new_quizzes:
                message += f"- {quiz.chapter.subject.name} - {quiz.chapter.name}\n"
        
        message += "\nDon't forget to practice and improve your skills!"
        
        if user.gchat_webhook:
            send_gchat_message(user.gchat_webhook, message)
        
        if user.email_notifications:
            send_email(
                user.username,
                "Quiz Master - Daily Reminder",
                "daily_reminder",
                user_name=user.full_name,
                new_quizzes=new_quizzes
            )

def generate_monthly_report(user):
    """Generate monthly activity report for a user"""
    last_month = datetime.utcnow().replace(day=1) - timedelta(days=1)
    start_date = last_month.replace(day=1)
    
    # Get user's quiz attempts for the month
    monthly_scores = Score.query.filter(
        Score.user_id == user.id,
        Score.time_stamp >= start_date,
        Score.time_stamp < start_date.replace(day=1) + timedelta(days=32)
    ).all()
    
    # Calculate statistics
    total_quizzes = len(monthly_scores)
    if total_quizzes > 0:
        avg_score = sum(score.total_scored for score in monthly_scores) / total_quizzes
    else:
        avg_score = 0
    
    # Get user's ranking
    rank_subquery = db.session.query(
        Score.user_id,
        func.avg(Score.total_scored).label('avg_score')
    ).filter(
        Score.time_stamp >= start_date
    ).group_by(Score.user_id).subquery()
    
    user_rank = db.session.query(
        func.count('*') + 1
    ).filter(
        rank_subquery.c.avg_score > avg_score
    ).scalar()

    # Send the report
    if user.email_notifications:
        send_email(
            user.username,
            f"Quiz Master - Monthly Activity Report - {last_month.strftime('%B %Y')}",
            "monthly_report",
            user_name=user.full_name,
            month=last_month.strftime('%B %Y'),
            total_quizzes=total_quizzes,
            avg_score=round(avg_score, 2),
            rank=user_rank,
            scores=monthly_scores
        )

def send_monthly_reports():
    """Send monthly reports to all users"""
    users = User.query.filter(
        User.role != 'admin',
        User.email_notifications == True
    ).all()
    
    for user in users:
        generate_monthly_report(user)
