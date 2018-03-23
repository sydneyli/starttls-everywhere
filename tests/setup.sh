### Certbot setup
ln -sf "/opt/starttls-everywhere/certificates" /etc/certificates

source ./certbot/venv/bin/activate

pip install -e starttls-policy

# Install certs via certbot!
postconf -e smtpd_tls_received_header=yes # for testing purposes
postconf -e disable_dns_lookups=yes # for testing purposes
certbot install --installer certbot-postfix:postfix --cert-path /etc/certificates/valid.crt --key-path /etc/certificates/valid.key -d valid.example-recipient.com

postfix stop
service postfix restart
