import json
from new_app.app_models.email_que import EmailQue
from new_app.email_service import EmailService

def start():
    list = EmailQue.objects.filter(sent=False)
    for item in list.iterator():
        EmailService.send_email(
            item.recipient_list,
            item.subject,
            item.message,
            item.sender,
        )
        EmailService.set_sent(item, True)