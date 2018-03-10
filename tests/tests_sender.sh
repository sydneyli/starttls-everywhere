set -e

./tests/setup.sh
postconf -e myhostname=sender.example.com

# Wait until we can contact the other machine, or timeout.
MAX_WAIT=5
NEXT_WAIT_TIME=0
until nc -z -v valid.example-recipient.com 25 || [ $NEXT_WAIT_TIME -eq $MAX_WAIT ]; do
    sleep $(( NEXT_WAIT_TIME++ ))
done

# Send a mail!
echo -e 'Subject: This is a subject.\n\nhi' | sendmail root@valid.example-recipient.com

# Wait for mail queue to empty.
NEXT_WAIT_TIME=0
until mailq | grep "empty" || [ $NEXT_WAIT_TIME -eq $MAX_WAIT ]; do
    sleep $(( NEXT_WAIT_TIME++ ))
done
