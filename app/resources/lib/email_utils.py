from flask import current_app, render_template
from flask_mail import Message
from app import mail, celery


@celery.task
def send_async_email(msg):
    try:
        import ipdb
        ipdb.set_trace()
        mail.send(msg)
    except Exception as e:
        current_app.logger.exception("Failed to Send Email {} : {}".format(msg, e))


def send_email(subject, template, to=list(), cc=list(), bcc=list(), **kwargs):
    assert to or cc or bcc
    msg = Message(current_app.config['MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=current_app.config['MAIL_SENDER'], recipients=to, cc=cc, bcc=bcc)
    msg.html = render_template(template + '.html', **kwargs)
    send_async_email.delay(msg)
