from sendgrid import SendGridAPIClient

from sendgrid.helpers.mail import Mail

sg_api_key = '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'

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