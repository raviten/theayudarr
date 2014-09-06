import smtplib
def send_email():
            gmail_user = "ismteja@gmail.com"
            gmail_pwd = "sriram@hanuman"
            FROM = 'ismteja@gmail.com'
            TO = ['ravitejanandula@gmail.com'] #must be a list
            SUBJECT = "Activate your Ayudar account"
            TEXT = "For better of people and next generation"

            # Prepare actual message
            message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
            try:
                #server = smtplib.SMTP(SERVER) 
                server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
                server.ehlo()
                server.starttls()
                server.login(gmail_user, gmail_pwd)
                server.sendmail(FROM, TO, message)
                #server.quit()
                server.close()
                print 'successfully sent the mail'
            except:
                print "failed to send mail"

def send_email(to,url):
            gmail_user = "ismteja@gmail.com"
            gmail_pwd = "sriram@hanuman"
            FROM = 'ismteja@gmail.com'
            TO = [to] #must be a list
            SUBJECT = "Activate your Ayudar account"
            TEXT = "For better of people and next generation please use the below link <br> "+url

            # Prepare actual message
            message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
            try:
                #server = smtplib.SMTP(SERVER) 
                server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
                server.ehlo()
                server.starttls()
                server.login(gmail_user, gmail_pwd)
                server.sendmail(FROM, TO, message)
                #server.quit()
                server.close()
                print 'successfully sent the mail'
            except:
                print "failed to send mail"
