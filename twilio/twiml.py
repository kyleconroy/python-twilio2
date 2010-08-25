import xml.etree.ElementTree as ET

class TwimlException(Exception): pass

class Verb(object):
    """Twilio basic verb object.
    """
    def __init__(self, **kwargs):
        self.name = self.__class__.__name__
        self.body = None
        self.nestables = None
        
        self.verbs = []
        self.attrs = {}
        for k, v in kwargs.items():
            if k == "sender": 
                k = "from"
            if v: 
                self.attrs[k] = v
    
    def __repr__(self):
        return ET.tostring(self.xml())

    def xml(self):
        el = ET.Element(self.name)
        
        keys = self.attrs.keys()
        keys.sort()
        for a in keys:
            el.set(a, str(self.attrs[a]))

        if self.body: 
            el.text = self.body

        for verb in self.verbs:
            el.append(verb.xml())

        return el
    
    def append(self, verb):
        if not self.nestables:
            raise TwimlException("%s is not nestable" % self.name)
        if verb.name not in self.nestables:
            raise TwimlException("%s is not nestable inside %s" % \
                (verb.name, self.name))
        self.verbs.append(verb)
        return verb
    
class Response(Verb):
    """Twilio response object.
    
    version: Twilio API version e.g. 2008-08-01
    """
    def __init__(self, version=None, **kwargs):
        Verb.__init__(self, version=version, **kwargs)
        self.nestables = ['Say', 'Play', 'Gather', 'Record', 'Dial',
            'Redirect', 'Pause', 'Hangup', 'Sms']

    def say(self, text, **kwargs):
        return self.append(Say(text, **kwargs))
    
    def play(self, url, **kwargs):
        return self.append(Play(url, **kwargs))
    
    def pause(self, **kwargs):
        return self.append(Pause(**kwargs))
    
    def redirect(self, url=None, **kwargs):
        return self.append(Redirect(url, **kwargs))   
    
    def hangup(self, **kwargs):
        return self.append(Hangup(**kwargs)) 
    
    def gather(self, **kwargs):
        return self.append(Gather(**kwargs))
    
    def dial(self, number=None, **kwargs):
        return self.append(Dial(number, **kwargs))
    
    def record(self, **kwargs):
        return self.append(Record(**kwargs))
        
    def sms(self, msg, **kwargs):
        return self.append(Sms(msg, **kwargs))

class Say(Verb):
    """Say text
    
    text: text to say
    voice: MAN or WOMAN
    language: language to use
    loop: number of times to say this text
    """
    MAN = 'man'
    WOMAN = 'woman'
    
    ENGLISH = 'en'
    SPANISH = 'es'
    FRENCH = 'fr'
    GERMAN = 'de'
    
    def __init__(self, text, voice=None, language=None, loop=None, **kwargs):
        Verb.__init__(self, voice=voice, language=language, loop=loop,
            **kwargs)
        self.body = text
        if voice and (voice != self.MAN and voice != self.WOMAN):
            raise TwimlException( \
                "Invalid Say voice parameter, must be 'man' or 'woman'")
        if language and (language != self.ENGLISH and language != self.SPANISH 
            and language != self.FRENCH and language != self.GERMAN):
            raise TwimlException( \
                "Invalid Say language parameter, must be " + \
                "'en', 'es', 'fr', or 'de'")

class Play(Verb):
    """Play audio file at a URL
    
    url: url of audio file, MIME type on file must be set correctly
    loop: number of time to say this text
    """
    def __init__(self, url, loop=None, **kwargs):
        Verb.__init__(self, loop=loop, **kwargs)
        self.body = url

class Pause(Verb):
    """Pause the call
    
    length: length of pause in seconds
    """
    def __init__(self, length=None, **kwargs):
        Verb.__init__(self, length=length, **kwargs)

class Redirect(Verb):
    """Redirect call flow to another URL
    
    url: redirect url
    """
    GET = 'GET'
    POST = 'POST'
    
    def __init__(self, url=None, method=None, **kwargs):
        Verb.__init__(self, method=method, **kwargs)
        if method and (method != self.GET and method != self.POST):
            raise TwimlException( \
                "Invalid method parameter, must be 'GET' or 'POST'")
        self.body = url

class Hangup(Verb):
    """Hangup the call
    """
    def __init__(self, **kwargs):
        Verb.__init__(self)

class Gather(Verb):
    """Gather digits from the caller's keypad
    
    action: URL to which the digits entered will be sent
    method: submit to 'action' url using GET or POST
    numDigits: how many digits to gather before returning
    timeout: wait for this many seconds before returning
    finishOnKey: key that triggers the end of caller input
    """
    GET = 'GET'
    POST = 'POST'

    def __init__(self, action=None, method=None, numDigits=None, timeout=None,
        finishOnKey=None, **kwargs):
        
        Verb.__init__(self, action=action, method=method,
            numDigits=numDigits, timeout=timeout, finishOnKey=finishOnKey,
            **kwargs)
        if method and (method != self.GET and method != self.POST):
            raise TwimlException( \
                "Invalid method parameter, must be 'GET' or 'POST'")
        self.nestables = ['Say', 'Play', 'Pause']

    def say(self, text, **kwargs):
        return self.append(Say(text, **kwargs))
    
    def play(self, url, **kwargs):
        return self.append(Play(url, **kwargs))
    
    def pause(self, **kwargs):
        return self.append(Pause(**kwargs))

class Number(Verb):
    """Specify phone number in a nested Dial element.
    
    number: phone number to dial
    sendDigits: key to press after connecting to the number
    """
    def __init__(self, number, sendDigits=None, **kwargs):
        Verb.__init__(self, sendDigits=sendDigits, **kwargs)
        self.body = number
        
class Sms(Verb):
    """ Send a Sms Message to a phone number
    
    to: whom to send message to, defaults based on the direction of the call
    sender: whom to send message from.
    action: url to request after the message is queued
    method: submit to 'action' url using GET or POST
    statusCallback: url to hit when the message is actually sent
    """
    GET = 'GET'
    POST = 'POST'
    
    def __init__(self, msg, to=None, sender=None, method=None, action=None,
        statusCallback=None, **kwargs):
        Verb.__init__(self, action=action, method=method, to=to, sender=sender,
            statusCallback=statusCallback, **kwargs)
        if method and (method != self.GET and method != self.POST):
            raise TwimlException( \
                "Invalid method parameter, must be GET or POST")
        self.body = msg

class Conference(Verb):
    """Specify conference in a nested Dial element.
    
    name: friendly name of conference 
    muted: keep this participant muted (bool)
    beep: play a beep when this participant enters/leaves (bool)
    startConferenceOnEnter: start conf when this participants joins (bool)
    endConferenceOnExit: end conf when this participants leaves (bool)
    waitUrl: TwiML url that executes before conference starts
    waitMethod: HTTP method for waitUrl GET/POST
    """
    GET = 'GET'
    POST = 'POST'
    
    def __init__(self, name, muted=None, beep=None,
        startConferenceOnEnter=None, endConferenceOnExit=None, waitUrl=None,
        waitMethod=None, **kwargs):
        Verb.__init__(self, muted=muted, beep=beep,
            startConferenceOnEnter=startConferenceOnEnter,
            endConferenceOnExit=endConferenceOnExit, waitUrl=waitUrl,
            waitMethod=waitMethod, **kwargs)
        if waitMethod and (waitMethod != self.GET and waitMethod != self.POST):
            raise TwimlException( \
                "Invalid waitMethod parameter, must be GET or POST")
        self.body = name

class Dial(Verb):
    """Dial another phone number and connect it to this call
    
    action: submit the result of the dial to this URL
    method: submit to 'action' url using GET or POST
    """
    GET = 'GET'
    POST = 'POST'
    
    def __init__(self, number=None, action=None, method=None, **kwargs):
        Verb.__init__(self, action=action, method=method, **kwargs)
        self.nestables = ['Number', 'Conference']
        if number and len(number.split(',')) > 1:
            for n in number.split(','):
                self.append(Number(n.strip()))
        else:
            self.body = number
        if method and (method != self.GET and method != self.POST):
            raise TwimlException( \
                "Invalid method parameter, must be GET or POST")

    def number(self, number, **kwargs):
        return self.append(Number(number, **kwargs))

    def conference(self, name, **kwargs):
        return self.append(Conference(name, **kwargs))


class Record(Verb):
    """Record audio from caller
    
    action: submit the result of the dial to this URL
    method: submit to 'action' url using GET or POST
    maxLength: maximum number of seconds to record
    timeout: seconds of silence before considering the recording complete
    """
    GET = 'GET'
    POST = 'POST'
    
    def __init__(self, action=None, method=None, maxLength=None, 
        timeout=None, **kwargs):
        Verb.__init__(self, action=action, method=method, maxLength=maxLength,
            timeout=timeout, **kwargs)
        if method and (method != self.GET and method != self.POST):
            raise TwimlException( \
                "Invalid method parameter, must be GET or POST")
