from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import text
from app.database_connect import engine  # Use existing engine from database.py
from app.global_constants import DELETE_DISLIKED_PROPERTIES_QUERY, DAYS_THRESHOLD

def scheduled_cleanup():
    """Deletes disliked properties older than DAYS_THRESHOLD days."""
    with engine.connect() as connection:
        connection.execute(text(DELETE_DISLIKED_PROPERTIES_QUERY), {"days_threshold": DAYS_THRESHOLD})
    print("Old disliked properties deleted.")

# Schedule the job to run at midnight
scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_cleanup, 'cron', hour=0, minute=0)
scheduler.start()

try:
    # Keeps the script running to allow APScheduler to operate
    scheduler._event.wait()
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
