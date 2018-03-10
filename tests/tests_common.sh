set -e

postconf -e myhostname=valid.example-recipient.com
./tests/setup.sh

if ! ((nc -w 1 localhost 25 <<< "EHLO $HOSTNAME") | grep "STARTTLS"); then
    echo "Server does not advertise STARTTLS!"
    exit 1;
fi

if ! ((nc -w 1 localhost 25 <<< "STARTTLS") | grep "Ready to start TLS"); then
    echo "Client does not try to initiate STARTTLS!"
    exit 1;
fi

