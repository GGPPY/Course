from .. import mail, celery


@celery.task(name='send_mail_async')
def send_mail_async(msg):
    mail.send(msg)
