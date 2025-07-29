import csv
import os
from datetime import datetime
from celery import Celery
from celery.schedules import crontab

# Explicitly configure Celery to use Redis for both broker and backend
celery = Celery('tasks',
                broker='redis://localhost:6379/0',
                backend='redis://localhost:6379/0')

# This imports the User and Score models only when the task is executed
from models import User, Score

@celery.task
def generate_user_performance_report():
    """A background task to generate a CSV report of user performance."""
    # This task needs access to the app's context to use the database
    from app import app
    with app.app_context():
        users = User.query.filter(User.role != 'admin').all()
        
        report_data = []
        for user in users:
            scores = user.scores
            quizzes_taken = len(scores)
            if quizzes_taken > 0:
                average_score = sum(s.total_scored for s in scores) / quizzes_taken
            else:
                average_score = 0
            
            report_data.append({
                'user_id': user.id,
                'full_name': user.full_name,
                'email': user.username,
                'quizzes_taken': quizzes_taken,
                'average_score': round(average_score, 2)
            })
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"user_performance_{timestamp}.csv"
        
        exports_dir = 'exports'
        if not os.path.exists(exports_dir):
            os.makedirs(exports_dir)
            
        filepath = os.path.join(exports_dir, filename)
        
        with open(filepath, 'w', newline='') as csvfile:
            fieldnames = ['user_id', 'full_name', 'email', 'quizzes_taken', 'average_score']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(report_data)
            
        return filename
        

# --- Placeholder tasks for future features ---
@celery.task
def daily_reminder():
    print("Sending daily reminders...")
    return "Daily reminders sent."

@celery.task
def monthly_activity_report():
    print("Generating and sending monthly reports...")
    return "Monthly reports sent."

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Daily reminder task scheduled for 7 PM every day
    sender.add_periodic_task(
        crontab(hour=19, minute=0),
        daily_reminder.s(),
    )
    # Monthly report task scheduled for the 1st day of the month at 8 AM
    sender.add_periodic_task(
        crontab(day_of_month=1, hour=8, minute=0),
        monthly_activity_report.s(),
    )