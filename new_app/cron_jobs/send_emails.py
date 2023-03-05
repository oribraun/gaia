from new_app.app_models.email_que import EmailQue
from new_app.email_service import EmailService

def start():
    print('started cron')
    list = EmailQue.objects.filter(sent=False)
    for item in list.iterator():
        EmailService.send_email(
            item.subject,
            item.message,
            item.sender,
            item.recipient_list,
        )
        EmailService.set_sent(item, True)