from sendgrid import SendGridAPIClient

from sendgrid.helpers.mail import Mail

sg_api_key = '****************************************************************************'

sender_email = 'oladayo.ak@gmail.com'

recipient_email = 'oladayo.ak@gmail.com'

subject = 'ETL Function Run Status Update'

def send_email(email_message):

    message = Mail(

        from_email = sender_email,

        to_emails = recipient_email,

        subject = subject,

        plain_text_content = email_message
    )

    sg = SendGridAPIClient(api_key = sg_api_key)

    return sg.send(message)
