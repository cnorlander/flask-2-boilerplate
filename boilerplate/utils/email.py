import re

def validate_address(email_address):
   pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
   if re.match(pattern, email_address):
      return True
   return False

def send_password_reset_email(address, url):
    # TODO: Due to the diversity of email solutions I have not included code to send the password reset code to the user
    # SMTP is a possible option but given how difficult it is to setup and maintain ones own email server these days and
    # have all messages arrive reliably I would suggest unless you have a mail service you pay for using something along
    # the lines of MailJet, MailGun, SendGrid or Twillio. If you add a phone number to the user object SMS is possible.
    # for now we will just print it to the console
    pass

def send_invite_email(email, temporary_password):
    pass