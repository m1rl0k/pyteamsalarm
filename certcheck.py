import requests
import datetime
import ssl
import OpenSSL.crypto as crypto

# Teams Incoming Webhook URL
webhook_url = "https://YOUR_TEAMS_WEBHOOK_URL"

# Certificate file path
cert_file = "/etc/letsencrypt/live/example.com/fullchain.pem"

# Number of days before expiration to send notification
expiration_threshold = 30

# Load the certificate
with open(cert_file, "rb") as f:
    cert = crypto.load_certificate(crypto.FILETYPE_PEM, f.read())

# Get the expiration date
expiration_date = datetime.datetime.strptime(cert.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ')

# Calculate the number of days until expiration
days_to_expiration = (expiration_date - datetime.datetime.utcnow()).days

# Check if the certificate is nearing expiration
if days_to_expiration <= expiration_threshold:
    # Construct the message payload
    message = {
        "text": f"The certificate located at {cert_file} is expiring in {days_to_expiration} days!"
    }

    # Send the message to the Teams channel
    response = requests.post(webhook_url, json=message)

    # Check if the request was successful
    if response.status_code == 200:
        print("Message sent to Teams channel successfully.")
    else:
        print("Failed to send message to Teams channel.")
else:
    print(f"The certificate located at {cert_file} is not expiring soon.")
