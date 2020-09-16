from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='*', hour = '9-23', minute='*/20')
def scheduled_job():
    print('每天09點~23點，每20分鐘觸發一次')

sched.start()