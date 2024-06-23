import smtplib
import dns.resolver
from email.mime.text import MIMEText

# Define the email details
from_address = 'from_address@mail.com'
to_address = 'to_address@mail.com'
subject = 'Subject: Test Email\n'
body = 'This is a test email.'

# Create the email message
msg = MIMEText(body)
msg['From'] = from_address
msg['To'] = to_address
msg['Subject'] = subject

# Resolve MX records for the recipient domain
domain = to_address.split('@')[1].strip()
print(f"Resolving MX records for {domain}")

try:
    mx_records = dns.resolver.resolve(domain, 'MX')
except dns.resolver.NoAnswer:
    print(f"No MX records found for domain {domain}")
    exit(1)
except dns.resolver.NXDOMAIN:
    print(f"Domain {domain} does not exist")
    exit(1)
except dns.exception.DNSException as e:
    print(f"DNS resolution error: {e}")
    exit(1)

# Choose a specific MX server (e.g., the first one)
mx_record = mx_records[0].exchange.to_text()
print(f"Chosen MX server: {mx_record}")

# Gmail SMTP server credentials
smtp_server = 'smtp.gmail.com'
smtp_port = 587
username = 'your_email'
password = 'your_app_password' 

try:
    # Connect to the Gmail SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
    server.login(username, password)
    server.set_debuglevel(1)  # Enable debug output
    server.sendmail(from_address, to_address, msg.as_string())
    server.quit()
    print("Email sent successfully via Gmail SMTP server")
except Exception as e:
    print(f"Failed to send email: {e}")
