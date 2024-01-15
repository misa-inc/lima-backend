"""
from datetime import datetime
from apscheduler.schedulers.background import  BackgroundScheduler

from .jobs import test, survey_event


interval: use when you want to run the job at fixed intervals of time

cron: use when you want to run the job periodically at certain time(s) of day



def start():
    scheduler=BackgroundScheduler()
    scheduler.add_job(survey_event,'cron',hour=0)
    scheduler.start()
"""
    
"""
with cron
year (int|str) – 4-digit year

month (int|str) – month (1-12)

day (int|str) – day of month (1-31)

week (int|str) – ISO week (1-53)

day_of_week (int|str) – number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)

hour (int|str) – hour (0-23)

minute (int|str) – minute (0-59)

second (int|str) – second (0-59)

start_date (datetime|str) – earliest possible date/time to trigger on (inclusive)

end_date (datetime|str) – latest possible date/time to trigger on (inclusive)

timezone (datetime.tzinfo|str) – time zone to use for the date/time calculations (defaults to scheduler timezone)
#trigger=CronTrigger(hour='23', minute='05')
jitter (int|None) – delay the job execution by jitter seconds at mos


"""