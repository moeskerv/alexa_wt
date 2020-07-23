# -*- coding: utf-8 -*-
'''
simple unit test for skill adapter

'''

import unittest
import lambda_function
import time
import json
import sys

skip_active = False
APP_ID = "amzn1.ask.skill.ef845e8d-591e-4a5a-802c-5ee89dd8e897"

class Test(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @unittest.skipIf(skip_active, "Test disabled")
    def test001_onLaunch(self):

        print("\nTesting: %s" % (self._testMethodName,))

        testevent = {
            "version": "1.0",
            "session": {
                "new": True,
                "sessionId": "amzn1.echo-api.session.test",
                "application": {
                    "applicationId": APP_ID
                },
                "user": {
                    "userId": "amzn1.ask.account.1234"
                }
            },
            "context": {
                "System": {
                    "application": {
                        "applicationId": "amzn1.ask.skill.1234"
                    },
                    "user": {
                        "userId": "amzn1.ask.account.1234"
                    },
                    "device": {
                        "deviceId": "amzn1.ask.device.1234",
                        "supportedInterfaces": {}
                    },
                    "apiEndpoint": "https://api.eu.amazonalexa.com",
                    "apiAccessToken": "12345"
                }
            },
            "request": {
                "type": "LaunchRequest",
                "requestId": "amzn1.echo-api.request.1234",
                "timestamp": "2020-07-23T12:23:11Z",
                "locale": "de-DE",
                "shouldLinkResultBeReturned": False
            }
        }

        expectedResult = '{"version": "1.0", "sessionAttributes": {}, "response": {"outputSpeech": {"type": "PlainText", "text": "Willkommen zum WlanThermo Alexa Skill "}, "card": {"type": "Simple", "title": "Willkommen", "content": "Willkommen zum WlanThermo Alexa Skill "}, "reprompt": {"outputSpeech": {"type": "PlainText", "text": "Du kannst mich nach Temperaturen, Pitmaster und Batteriestand fragen."}}, "shouldEndSession": false}}'

        result = json.dumps(lambda_function.lambda_handler(
            testevent, {}), ensure_ascii=False)
        print(result)
        self.assertEqual(result, expectedResult)

    @unittest.skipIf(skip_active, "Test disabled")
    def test002_getTemperatures(self):

        print("\nTesting: %s" % (self._testMethodName,))

        testevent = {
            "version": "1.0",
            "session": {
                "new": True,
                "sessionId": "amzn1.echo-api.session.test",
                "application": {
                    "applicationId": APP_ID
                },
                "user": {
                    "userId": "amzn1.ask.account.1234"
                }
            },
            "context": {
                "System": {
                    "application": {
                        "applicationId": "amzn1.ask.skill.1234"
                    },
                    "user": {
                        "userId": "amzn1.ask.account.1234"
                    },
                    "device": {
                        "deviceId": "amzn1.ask.device.1234",
                        "supportedInterfaces": {}
                    },
                    "apiEndpoint": "https://api.eu.amazonalexa.com",
                    "apiAccessToken": "12345"
                }
            },
            "request": {
		        "type": "IntentRequest",
                "requestId": "amzn1.echo-api.request.38a3b85b-9b4d-4d91-bf78-d1abab0f8d1c",
                "locale": "de-DE",
                "timestamp": "2020-07-23T13:37:39Z",
                "intent": {
                    "name": "GetTemperatures",
                    "confirmationStatus": "NONE"
                }
            }
        }

        expectedResult = '{"version": "1.0", "sessionAttributes": {}, "response": {"outputSpeech": {"type": "PlainText", "text": "Temperatur Ist-Werte: Kerntemp: 26,7 Grad Kanal 2: 26,6 Grad "}, "card": {"type": "Simple", "title": "Temperaturen", "content": "Temperatur Ist-Werte: Kerntemp: 26,7 Grad Kanal 2: 26,6 Grad "}, "reprompt": {"outputSpeech": {"type": "PlainText", "text": ""}}, "shouldEndSession": false}}'

        # TODO: as temperatures change we may want to have a mock here :-)

        result = json.dumps(lambda_function.lambda_handler(
            testevent, {}), ensure_ascii=False)
        print(result)
        self.assertEqual(result, expectedResult)

    @unittest.skipIf(skip_active, "Test disabled")
    def test003_getPitmaster(self):

        print("\nTesting: %s" % (self._testMethodName,))

        testevent = {
            "version": "1.0",
            "session": {
                "new": True,
                "sessionId": "amzn1.echo-api.session.test",
                "application": {
                    "applicationId": APP_ID
                },
                "user": {
                    "userId": "amzn1.ask.account.1234"
                }
            },
            "context": {
                "System": {
                    "application": {
                        "applicationId": "amzn1.ask.skill.1234"
                    },
                    "user": {
                        "userId": "amzn1.ask.account.1234"
                    },
                    "device": {
                        "deviceId": "amzn1.ask.device.1234",
                        "supportedInterfaces": {}
                    },
                    "apiEndpoint": "https://api.eu.amazonalexa.com",
                    "apiAccessToken": "12345"
                }
            },
            "request": {
		        "type": "IntentRequest",
                "requestId": "amzn1.echo-api.request.38a3b85b-9b4d-4d91-bf78-d1abab0f8d1c",
                "locale": "de-DE",
                "timestamp": "2020-07-23T13:37:39Z",
                "intent": {
                    "name": "GetPitmaster",
                    "confirmationStatus": "NONE"
                }
            }
        }

        expectedResult = '{"version": "1.0", "sessionAttributes": {}, "response": {"outputSpeech": {"type": "PlainText", "text": "Pitmaster Ist-Werte: Pitmaster1: 0 % Pitmaster2: 0 % "}, "card": {"type": "Simple", "title": "Pitmaster", "content": "Pitmaster Ist-Werte: Pitmaster1: 0 % Pitmaster2: 0 % "}, "reprompt": {"outputSpeech": {"type": "PlainText", "text": ""}}, "shouldEndSession": false}}'
        result = json.dumps(lambda_function.lambda_handler(
            testevent, {}), ensure_ascii=False)
        print(result)
        self.assertEqual(result, expectedResult)

    @unittest.skipIf(skip_active, "Test disabled")
    def test004_getBattery(self):

        print("\nTesting: %s" % (self._testMethodName,))

        testevent = {
            "version": "1.0",
            "session": {
                "new": True,
                "sessionId": "amzn1.echo-api.session.test",
                "application": {
                    "applicationId": APP_ID
                },
                "user": {
                    "userId": "amzn1.ask.account.1234"
                }
            },
            "context": {
                "System": {
                    "application": {
                        "applicationId": "amzn1.ask.skill.1234"
                    },
                    "user": {
                        "userId": "amzn1.ask.account.1234"
                    },
                    "device": {
                        "deviceId": "amzn1.ask.device.1234",
                        "supportedInterfaces": {}
                    },
                    "apiEndpoint": "https://api.eu.amazonalexa.com",
                    "apiAccessToken": "12345"
                }
            },
            "request": {
		        "type": "IntentRequest",
                "requestId": "amzn1.echo-api.request.38a3b85b-9b4d-4d91-bf78-d1abab0f8d1c",
                "locale": "de-DE",
                "timestamp": "2020-07-23T13:37:39Z",
                "intent": {
                    "name": "GetBattery",
                    "confirmationStatus": "NONE"
                }
            }
        }

        expectedResult = '{"version": "1.0", "sessionAttributes": {}, "response": {"outputSpeech": {"type": "PlainText", "text": "Ladezustand: 47%"}, "card": {"type": "Simple", "title": "Batterie", "content": "Ladezustand: 47%"}, "reprompt": {"outputSpeech": {"type": "PlainText", "text": ""}}, "shouldEndSession": false}}'
        result = json.dumps(lambda_function.lambda_handler(
            testevent, {}), ensure_ascii=False)
        print(result)
        self.assertEqual(result, expectedResult)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testDiscovery']
    unittest.main()
