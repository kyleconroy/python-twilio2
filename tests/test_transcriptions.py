from mock import patch, Mock
from nose.tools import raises
from twilio.rest.resources import Transcriptions
from tools import create_mock_json

BASE_URI = "https://api.twilio.com/2010-04-01/Accounts/AC123"
ACCOUNT_SID = "AC123"
AUTH = (ACCOUNT_SID, "token")


transcriptions = Transcriptions(BASE_URI, AUTH)

@patch("twilio.rest.resources.make_twilio_request")
def test_paging(mock):
    resp = create_mock_json("tests/resources/transcriptions_list.json")
    mock.return_value = resp

    uri = "{}/Transcriptions".format(BASE_URI)
    transcriptions.list(page=2)

    mock.assert_called_with("GET", uri, params={"Page": 2})

@patch("twilio.rest.resources.make_twilio_request")
def test_get(mock):
    resp = create_mock_json("tests/resources/transcriptions_instance.json")
    mock.return_value = resp

    uri = "{}/Transcriptions/TR123".format(BASE_URI)
    transcriptions.get("TR123")

    mock.assert_called_with("GET", uri)


@raises(AttributeError)
def test_create():
    transcriptions.create

@raises(AttributeError)
def test_update():
    transcriptions.update

@raises(AttributeError)
def test_update():
    transcriptions.delete
