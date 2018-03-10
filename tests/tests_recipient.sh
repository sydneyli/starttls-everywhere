set -e

[ -e /var/mail/root ] && rm /var/mail/root

./tests/setup.sh
postconf -e myhostname=valid.example-recipient.com


# Wait until we receive a message or time out.
MAX_WAIT=5
NEXT_WAIT_TIME=0
until [ -f '/var/mail/root' ] || [ $NEXT_WAIT_TIME -eq $MAX_WAIT ]; do
    sleep $(( NEXT_WAIT_TIME++ ))
done

# Check for the message.
cat /var/mail/root | grep "using TLSv1.2"

