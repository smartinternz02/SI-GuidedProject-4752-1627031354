import wiotp.sdk.device
import time
import random
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import simpleaudio as sa

authenticator = IAMAuthenticator('uQ-kJ7yvhpbFF1FhwsX_xaFeP-WSTuVqKYgOgLW3Zpfy')
text_to_speech = TextToSpeechV1(
    authenticator=authenticator
)

text_to_speech.set_service_url('https://api.eu-gb.text-to-speech.watson.cloud.ibm.com/instances/73add8e6-13e5-43c5-a808-03d3eed007b7')

myConfig = { 
    "identity": {
        "orgId": "iyqgoe",
        "typeId": "AkshuDevice",
        "deviceId":"240602"
    },
    "auth": {
        "token": "240602291205"
    }
}

def myCommandCallback(cmd):
    print("Message received from IBM IoT Platform: %s" % cmd.data['command'])
    m=cmd.data['command']
    if(m == "wateropen"):
        print(".......Water is OPEN.......")
    elif(m == "waterclose"):
        print(".......Water is CLOSE........")
    elif(m == "foodopen"):
        print(".......Food is OPEN........")
    elif(m == "foodclose"):
        print(".......Food is CLOSE........")
    print()
    with open('Hello.wav', 'wb') as audio_file:
            audio_file.write(
                text_to_speech.synthesize(
                    m,
                    voice='en-US_MichaelVoice',
                    accept='audio/wav'
                    ).get_result().content)
    filename = 'Hello.wav'
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    play_obj.wait_done()

client = wiotp.sdk.device.DeviceClient(config=myConfig, logHandlers=None)
client.connect()

while True:
    waterlevel=random.randint(0,100)
    foodlevel=random.randint(0,100)
    myData={'waterlevel':waterlevel, 'foodlevel':foodlevel}
    client.publishEvent(eventId="status", msgFormat="json", data=myData, qos=0, onPublish=None)
    print("Published data Successfully: %s", myData)
    client.commandCallback = myCommandCallback
    time.sleep(2)
client.disconnect()
