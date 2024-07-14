import smtplib, ssl
from email.message import EmailMessage


class Email:
    def send(self, tour_info):
        """ Send email with details of new tour info """
        host = "smtp.gmail.com"
        port = 465

        sender = "leobot1010@gmail.com"
        password = 'vuihokpyyfphutnc'

        receiver = 'kieran303@hotmail.com'
        # receiver = 'leobot1010@gmail.com'

        context = ssl.create_default_context()

        em = EmailMessage()
        em['From'] = sender
        em['To'] = receiver
        em['Subject'] = 'New Tour Announced'
        em.set_content(tour_info)


        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(sender, password)
            server.sendmail(sender, receiver, em.as_string())

        print("Email was sent")