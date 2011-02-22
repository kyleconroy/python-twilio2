Making Twilio even easier (is it possible?)

## Installation

We aren't on PyPi just yet, but you can install straight from github using pip

    pip install -e git+https://github.com/derferman/python-twilio2.git#egg=twilio

## Examples

### REST API

    import twilio

    conn = twilio.api.Client()
    call = conn.calls.make(to="9991231234, from_="9991231234",
                           url="http://foo.com/call.xml")
    print call.length
    print call.sid


### Twiml

    from twilio import twiml

    r = twiml.Response()
    r.play("monkey.mp3", loop=5)
    r.toxml() 
    # returns <Response><Play loop="3">monkey.mp3</Play><Response>

### Documentation

http://derferman.github.com/python-twilio2/
