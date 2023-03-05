from new_app.app_models.email_que import EmailQue
from new_app.email_service import EmailService

def start():
    list = EmailQue.objects.filter(sent=False)
    for i in list:
        query_set = list[i]
        EmailService.send_email(
            query_set.subject,
            query_set.message,
            query_set.sender,
            query_set.recipient_list,
        )
        EmailService.set_sent(query_set, True)