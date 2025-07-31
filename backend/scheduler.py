from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from notifications import send_daily_reminders, send_monthly_reports
from flask import current_app

scheduler = BackgroundScheduler()

def init_scheduler(app):
    with app.app_context():
        # Schedule daily reminders to run every day
        scheduler.add_job(
            send_daily_reminders,
            trigger=CronTrigger(hour=18),  # Run at 6 PM every day
            id='daily_reminders',
            name='Send daily reminders to users',
            replace_existing=True
        )
        
        # Schedule monthly reports to run on the first day of each month
        scheduler.add_job(
            send_monthly_reports,
            trigger=CronTrigger(day=1, hour=8),  # Run at 8 AM on the first day of each month
            id='monthly_reports',
            name='Send monthly activity reports',
            replace_existing=True
        )
        
        scheduler.start()
