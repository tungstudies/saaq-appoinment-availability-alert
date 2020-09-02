# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from utils import SENDGRID_API_KEY


def send_email():
    message = Mail(
        from_email='tungstudies@gmail.com',
        to_emails='nguyenthanhtung2605@gmail.com',
        subject='SAAQ Road Test Appointment might now be Available at Langelier',
        html_content='<a href="https://saaq.gouv.qc.ca/en/online-services/citizens/driving-test/making-appointment'
                     '/vehicule-class-5/">Visit SAAQ</a>')
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.body)

    return