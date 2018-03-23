### Certbot setup
ln -sf "/opt/starttls-everywhere/certificates" /etc/certificates

source ./certbot/venv/bin/activate

pip install -e starttls-policy

# Postconf things for testing purposes.
postconf -e smtpd_tls_received_header=yes
postconf -e disable_dns_lookups=yes

# Install certs via certbot!
certbot install --installer certbot-postfix:postfix --cert-path /etc/certificates/valid.crt --key-path /etc/certificates/valid.key -d valid.example-recipient.com

