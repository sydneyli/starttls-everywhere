set -e

# Entrypoint for testing. Hostname should either be "sender" or "receiver".

# Setup
if ! postconf myhostname | grep $HOSTNAME ; then
    postconf -e myhostname=$HOSTNAME
    ./tests/setup.sh
fi

postfix stop
service postfix restart

. ./tests/common.sh

# Cleanup from previous runs
[ -e /var/mail/root ] && rm /var/mail/root

# Run test
if [[ $HOSTNAME = "sender" ]]
then
    function recipient_up() {
        nc -z -v recipient 25
    }

    function mailqueue_empty() {
        mailq | grep "empty"
    }

    wait_for recipient_up

    echo -e 'Subject: This is a subject.\n\nhi' | sendmail root@recipient

    wait_for mailqueue_empty
else
    function got_mail() {
        [ -f '/var/mail/root' ]
    }

    wait_for got_mail

    assert "Mail was sent over TLS" "cat /var/mail/root | grep 'using TLSv1.2'"
fi
