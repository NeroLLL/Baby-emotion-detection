import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# host infromation
# host address
mail_host = 'smtp.gmail.com'
# user name
mail_user = 'nerolwow'
# password
mail_pass = 'jiazk9808'
sender = 'nerolwow@gmail.com'
receivers = ['zlen5056@uni.sydney.edu.au']

# setting of mail
# text of mail
message = MIMEMultipart()
# subject of mail
message['Subject'] = 'Alarm of Baby Emotion!!! - Boring!'
# sender information
message['From'] = sender
# receivers information
message['To'] = receivers[0]

with open('boring.txt', 'r')as h:
    content1 = h.read()
part1 = MIMEText(content1, 'plain', 'utf-8')

# part1['Content-Type'] = 'application/octet-stream'
# part1['Content-Disposition'] = 'attachment;filename="abc.txt"'

with open('image.jpg', 'rb')as fp:
    picture = MIMEImage(fp.read())
#    picture['Content-Type'] = 'application/octet-stream'
#    picture['Content-Disposition'] = 'attachment;filename="1.png"'
message.attach(part1)
# message.attach(part2)
message.attach(picture)

# connect & login
try:
    smtpObj = smtplib.SMTP()
    # connect
    # smtpObj.connect(mail_host,25)
    smtpObj = smtplib.SMTP_SSL(mail_host)
    # login
    smtpObj.login(mail_user, mail_pass)
    # send
    smtpObj.sendmail(
        sender, receivers, message.as_string())
    # quit
    smtpObj.quit()
    print('success')
except smtplib.SMTPException as e:
    print('error', e)  # error print
