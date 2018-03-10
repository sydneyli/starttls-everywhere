#
# service syslog-ng start

### DNS setup
# Have DNSmasq point mx records at self, and enable root user
echo "selfmx
      user=root" > /etc/dnsmasq.conf

# Do not try this at home!
# Force image to use DNSmasq resolver
echo "nameserver 127.0.0.1" > /etc/resolv.conf

service dnsmasq restart

### Certbot setup
ln -sf "/opt/starttls-everywhere/certificates" /etc/certificates

source ./certbot/venv/bin/activate

pip install -e starttls-policy

# Install certs via certbot!
postconf -e smtpd_tls_received_header=yes # for testing purposes
certbot install --installer certbot-postfix:postfix --cert-path /etc/certificates/valid.crt --key-path /etc/certificates/valid.key -d valid.example-recipient.com

postfix stop
service postfix restart
