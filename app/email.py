from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail

# 异步发送电子邮件的线程函数
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + ' ' + subject,       # 初始化邮件的消息
                  sender=app.config['MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)                # 渲染纯文本正文
    msg.html = render_template(template + '.html', **kwargs)               # 渲染富文本正文
    thr = Thread(target=send_async_email, args=[app, msg])                 # 创建线程，异步发送电子邮件
    thr.start()                                                            # 启动线程
    return thr
