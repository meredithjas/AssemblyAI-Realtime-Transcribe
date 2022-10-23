import websockets
import asyncio
import base64
import json
import pyaudio
from configure import auth_key
 
FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
p = pyaudio.PyAudio()
 
# starts recording
stream = p.open(
   format=FORMAT,
   channels=CHANNELS,
   rate=RATE,
   input=True,
   frames_per_buffer=FRAMES_PER_BUFFER
)

# the AssemblyAI endpoint we're going to hit
URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"

# Determines the last letter of word and adds -v for vowels and -c for consonants
def convert_text(textstring):
    separator = ' '
    punctuation = '.,;:?!'
    vowel = 'aeiou'
    # Splits string into individual words
    words = textstring.split(separator)
    newWords = []

    # If there is a word in the string
    if len(textstring)!=0:
        print(words)
        for word in words:
            # If word has a punctuation next to it, gets the second to the last letter, and appends to new array
            if word[-1] in punctuation:
                if word[-2] in vowel:
                    newWord = word[0:-1] + '-v' + word[-1]
                    newWords.append(newWord)
                elif word[-2] not in vowel:
                    newWord = word[0:-1] + '-c' + word[-1]
                    newWords.append(newWord)

            # If last letter is vowel, adds -v to the end of letter, and appends to new array
            elif word[-1] in vowel:
                newWord = word + '-v'
                newWords.append(newWord)

            # If last letter is neither punctuation nor vowel, adds -c to the end of letter, and appends to new array
            else:
                newWord = word + '-c'
                newWords.append(newWord)

        newSentence = separator.join(newWords)
        return newSentence
 
async def send_receive():
    print(f'Connecting websocket to url ${URL}')
    async with websockets.connect(
        URL,
        extra_headers=(("Authorization", auth_key),),
        ping_interval=5,
        ping_timeout=20
    ) as _ws:
        await asyncio.sleep(0.1)
        print("Receiving SessionBegins ...")
        session_begins = await _ws.recv()
        print(session_begins)
        print("Sending messages ...")
        async def send():
            while True:
                try:
                    data = stream.read(FRAMES_PER_BUFFER)
                    data = base64.b64encode(data).decode("utf-8")
                    json_data = json.dumps({"audio_data":str(data)})
                    await _ws.send(json_data)
                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break
                except Exception as e:
                    assert False, "Not a websocket 4008 error"
                await asyncio.sleep(0.01)
          
            return True
      
        async def receive():
            while True:
                try:
                    result_str = await _ws.recv()
                    if json.loads(result_str)["message_type"] == 'FinalTranscript':
                        print(convert_text(json.loads(result_str)['text']))
                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break
                except Exception as e:
                    assert False, "Not a websocket 4008 error"
      
        send_result, receive_result = await asyncio.gather(send(), receive())

while True:
    asyncio.run(send_receive())