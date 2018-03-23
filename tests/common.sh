assert () {
    echo "TEST: $1"
    if [ ! "$2" ] ; then
        echo "  FAIL: \"$2\""
        return 1
    else
        echo "  PASS"
        return 0
    fi
}

wait_for () {
    MAX_WAIT=5
    NEXT_WAIT_TIME=0
    until ($1) || [ $NEXT_WAIT_TIME -eq $MAX_WAIT ]; do
        sleep $(( NEXT_WAIT_TIME++ ))
    done
}
