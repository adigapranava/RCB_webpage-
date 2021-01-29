def generate_key():
    from random import randint
    SECRETE_KEY = randint(10**5, 10**6 - 1)
    return SECRETE_KEY


def send_key(to_address):

    SECRETE_KEY = generate_key()

    message = '''Is this you you signing up?
    if yes, use this varification code:
                {}
    Thank you, from RCB teams... '''.format(SECRETE_KEY)

    subject = "Varification Code"

    return (send_mail(to_address= to_address, msgs= message, subject= subject),SECRETE_KEY)



def send_mail(to_address, msgs, subject = "message from rcbfanclub"):
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import smtplib
    
    msg = MIMEMultipart()

    message = msgs

    password = ""
    msg['From'] = "rcbfanclub402@gmail.com"
    msg['To'] = to_address
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com: 587')

    server.starttls()

    try:
        server.login(msg['From'], password)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        return True
    except:
        return False

if __name__ == "__main__":
    print(send_key("p@1"))
    #print(generate_key())
    print(send_mail('pranavaadiga19@gmail.com', "hai hello"))
