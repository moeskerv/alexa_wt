"""
WlanThermo Alexa Skill Adapter

Dependencies:

- Python requests

TODOs

- support HTTP 204 - empty data -> DONE
- support HTTP 412 - device - alexa connection missing, echo out code
- nicen cards, add line breaks -> DONE
- use POST request to get data
- allow use to specify channel for temperatures
- support multiple WLANThermo devices per Alexa user
- use alexa session.user.userId as indentification against WLANThermo cloud
- add api token for skill adapter
- align print and logger debug output -> DONE
- implement unit test against static mock in WLANThermo cloud
- make better use of echo displays (e.g. WLANThermo logo in background)
- check data age and prompt if data is too old -> DONE (untested)
- only prompt pitmaster which are active -> DONE (untested)

Links:

https://developer.amazon.com/en-US/docs/alexa/custom-skills/request-and-response-json-reference.html


"""

import json
import requests
import logging
import time

# init logger
logger = logging.getLogger()
logging.basicConfig()
logger.setLevel(logging.INFO)

# versioning
VERSION = '1.0.0'
USERAGENT = 'WlanThermoAlexaSkill/' + VERSION

# errorcodes
NO_ERROR = 200
NO_DATA_AVAILABLE = 204
INVALID_AUTHORIZATION_CREDENTIAL = 401
INTERNAL_ERROR = 500
ACCOUNT_LINKING_MISSING = 412

# Misc constants
DATA_MAX_AGE = 15 * 60  # 15 Minutes max data age

# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(card_title, card_text, speech_output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': speech_output
        },
        'card': {
            'type': 'Simple',
            'title': card_title,
            'content': card_text
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- get data from WlanThermo Cloud -------------------------------
def get_wlanthermo_data(user_id):

    BASEURL = "https://dev-cloud.wlanthermo.de/"
    API_TOKEN = "2462abc331700b5426a258"

    request_status = NO_ERROR
    url = BASEURL + "data.php?api_token=" + API_TOKEN

    # adjust the user agent used in this request
    headers = requests.utils.default_headers()
    headers.update({'User-Agent': USERAGENT, })
    dataJson = None

    try:
        response = requests.get(url, headers=headers)
        request_status = response.status_code

        if request_status == NO_ERROR or request_status == ACCOUNT_LINKING_MISSING:
            dataJson = response.json()

    except requests.exceptions.Timeout:
        request_status = INTERNAL_ERROR
        logger.info("Send request: Timeout detected")

    except:
        logger.exception('Send request: Unknown Error occurred')
        request_status = INTERNAL_ERROR

    return request_status, dataJson


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    # Welcome message and init of the session (if required)

    session_attributes = {}
    card_title = "Willkommen"
    speech_output = "Willkommen zum WlanThermo Alexa Skill "

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Du kannst mich nach Temperaturen, Pitmaster und Batteriestand fragen."

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, speech_output, reprompt_text, should_end_session))


def get_temperatures(wlanthermo_data):

    session_attributes = {}
    reprompt_text = ""
    should_end_session = False
    card_title = "Temperaturen"
    active_channel_count = 0

    card_text = "Temperatur Ist-Werte: \n"
    speech_output = "Die Temperaturen der aktiven Fühler sind: "

    # iterate through all temps, take those which are != 999
    for channel in wlanthermo_data['channel']:
        if channel['temp'] != 999:
            active_channel_count += 1
            channel_text = channel['name'] + ": " + \
                str(channel['temp']).replace('.', ',') + " Grad "
            speech_output = speech_output + channel_text
            card_text = card_text + channel_text + "\n"

    if active_channel_count == 0:
        card_text = "Es ist kein Temperaturfühler aktiv"
        speech_output = card_text

    return build_response(session_attributes, build_speechlet_response(
        card_title, card_text, speech_output, reprompt_text, should_end_session))


def get_pitmaster(wlanthermo_data):

    session_attributes = {}
    card_title = "Pitmaster"
    card_text = "Pitmaster Ist-Werte: \n"
    speech_output = "Die aktuellen Werte der Pitmaster sind: "
    reprompt_text = ""
    should_end_session = False
    active_channel_count = 0

    # iterate through all temps, take those which are != 999
    for pitmaster in wlanthermo_data['pitmaster']:
        if channel['typ'] != "off":
            active_channel_count += 1
            channel_text = "Pitmaster" + \
                str(pitmaster['channel']) + ": " + \
                str(pitmaster['value']) + " % "
            speech_output = speech_output + channel_text
            card_text = card_text + channel_text + "\n"

    if active_channel_count == 0:
        card_text = "Es ist kein Pitmaster aktiv"
        speech_output = card_text

    return build_response(session_attributes, build_speechlet_response(
        card_title, card_text, speech_output, reprompt_text, should_end_session))


def get_battery(wlanthermo_data):

    session_attributes = {}
    card_title = "Batterie"
    speech_output = "Ladezustand: 47%"
    reprompt_text = ""
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, speech_output, reprompt_text, should_end_session))


def handle_204():

    session_attributes = {}
    reprompt_text = ""
    should_end_session = True
    card_title = "Keine Daten verfügbar."

    speech_output = "Es liegen keine aktuellen Daten vor."

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, speech_output, reprompt_text, should_end_session))


def handle_412(wlanthermo_data):

    session_attributes = {}
    reprompt_text = ""
    should_end_session = True
    token = "12345678abcdef"
    card_title = "WlanThermo noch nicht verbunden."
    card_text = "WLANThermo Verbindung mit Alexa wurde noch nicht konfiguriert.\n"\
        "Bitte gib folgenden Token in der WlanThermo Cloud ein, \n"\
        "um die Verbindung herzustellen: " + token

    speech_output = "WLANThermo Verbindung mit Alexa wurde noch nicht konfiguriert."\
        "Bitte gib folgenden Token in der WlanThermo Cloud ein, "\
        "um die Verbindung herzustellen: " + token

    return build_response(session_attributes, build_speechlet_response(
        card_title, card_text, speech_output, reprompt_text, should_end_session))


def handle_error(request_status):

    session_attributes = {}
    reprompt_text = ""
    should_end_session = True

    speech_output = "Es ist ein Fehler aufgetreten, versuche es später noch einmal. Fehlercode: " + \
        str(request_status)

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Auf Wiedersehen!"
    speech_output = "Vielen Dank für die Nutzung des WlanThermo Skills. "
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, speech_output, None, should_end_session))

# --------------- Events ------------------


def on_session_started(session_started_request, session):
    """ Called when the session starts """
    logger.info("on_session_started requestId=" + session_started_request['requestId']
                + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    # Called when the user launches the skill without intend

    logger.info("on_launch requestId=" + launch_request['requestId'] +
                ", sessionId=" + session['sessionId'])

    return get_welcome_response()


def on_intent(intent_request, session):
    # Called when the user specifies an intent

    logger.info("on_intent requestId=" + intent_request['requestId'] +
                ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # fetch data from cloud
    request_status, wlanthermo_data = get_wlanthermo_data(
        session['user']['userId'])
    logger.info("Response: " + json.dumps(wlanthermo_data))

    # check age of data, if too old, simulate 204 -> no data
    if request_status == 200:
        if time.time() - int(wlanthermo_data['system']['time']) > DATA_MAX_AGE:
            request_status = 204

    if request_status == 200:  # Dispatch skill's intent handlers

        if intent_name == "GetTemperatures":
            return get_temperatures(wlanthermo_data)
        elif intent_name == "GetPitmaster":
            return get_pitmaster(wlanthermo_data)
        elif intent_name == "GetBattery":
            return get_battery(wlanthermo_data)
        elif intent_name == "AMAZON.HelpIntent" or intent_name == "AMAZON.NavigateHomeIntent":
            return get_welcome_response()
        elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
            return handle_session_end_request()
        else:
            raise ValueError("Invalid intent")

    # no data available (last data older than 48h or no data yet)
    elif request_status == 204:
        return handle_204()

    elif request_status == 412:  # precondition failed -> no link between alexa and wlanthermo
        return handle_412(wlanthermo_data)

    else:  # unhandled return code
        return handle_error(request_status)


def on_session_ended(session_ended_request, session):
    # Called when the user ends the session.
    # Is not called when the skill returns should_end_session=true

    logger.info("on_session_ended requestId=" + session_ended_request['requestId'] +
                ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    # Route the incoming request based on type (LaunchRequest, IntentRequest, etc.)

    logger.info("Event: " + json.dumps(event))

    # ensure only my skill can use this lambda function
    # if (event['session']['application']['applicationId'] != "amzn1.ask.skill.abc"):
    #    raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
