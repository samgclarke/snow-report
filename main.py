import os
import scrapy
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class SnowSpider(scrapy.Spider):
    name = 'snowspider'
    start_urls = ['http://www.cypressmountain.com/downhill-conditions']

    def parse(self, response):
        html_body = ''
        el_list = []
        for item in response.css('div.weather-item'):
            label = item.css('label ::text').extract_first()
            amount = item.css('span ::text').extract_first()
            if 'Snow Stake Cam' in label:
                continue
            el_list.append({
                'Label: ': label,
                'Amount of snow: ': amount
            })
            html_body += '<p>{}: <strong>{}</strong></p>'.format(label, amount)
        self._send_report(html_body=html_body)

    def _send_report(self, html_body=None):
        receivers = ['samclarke.g@gmail.com']
        sender = 'snow-report@fromdomain.com'

        email_username = os.environ['EMAIL_USERNAME']
        email_password = os.environ['EMAIL_PASSWORD']

        msg = MIMEMultipart('alternative')
        msg['To'] = ', '.join(receivers)
        msg['From'] = sender
        msg['Subject'] = 'Cypress Snow Report'
        body = MIMEText(html_body, 'html')
        msg.attach(body)

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()      # for tls add this line
            server.starttls()  # for tls add this line
            server.ehlo()      # for tls add this line
            server.login(email_username, email_password)
            server.sendmail(sender, receivers, msg.as_string())
            print "Successfully sent email"
        except smtplib.SMTPException:
            print "--------------------->Error: unable to send email"
