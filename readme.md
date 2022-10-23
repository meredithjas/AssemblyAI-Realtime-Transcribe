# AssemblyAI Real Time Transcription

# Overview

This project applies [Assembly AI’s real time transcription service](https://www.assemblyai.com/blog/real-time-speech-recognition-with-python/), and packing it in a simple Python service. The service transcribes audio real time via the machines microphone. As an added feature, the service also adds `-v` to words that end in vowels, and `-c` to words that end in consonants. Here is an example demonstration:

![Transcription from terminal](AssemblyAI%20Real%20Time%20Transcription%20b05c9bd1a2f64652a43683e7fbabc841/BoomAI_Q4_-_Assembly_AI_Real_Time_Transcription.png)

Transcription from terminal

In addition, the service is packed in Streamlit as a simple UI web app. Below is a sample demonstration:

![Transcription from streamlit](AssemblyAI%20Real%20Time%20Transcription%20b05c9bd1a2f64652a43683e7fbabc841/Screen_Shot_2022-10-23_at_6.09.17_PM.png)

Transcription from streamlit

---

# Running the Service

## VirtualEnv and Dependencies Installation

Before running the API, create a virtual environment and install the dependencies in the **requirements.txt** file. Portaudio is needed to be installed as well.

```bash
brew install portaudio
```

```bash
$ virtualenv transcribe
$ source transcribe/bin/activate
(transcribe)$ pip3 install -r path/to/requirements.txt
```

## Testing

To run the simple python service, simply run it via:

```bash
(transcribe)$ python3 realtime_transcribe.py
```

DEMO:

[https://drive.google.com/file/d/1fagRYYQIAqW8TnShKwPRTk3lqmB6uYgR/view?usp=sharing](https://drive.google.com/file/d/1fagRYYQIAqW8TnShKwPRTk3lqmB6uYgR/view?usp=sharing)

To run the streamlit service, run it via:

```bash
(transcribe)$ python3 realtime_transcribe_streamlit.py
```

DEMO:

[https://drive.google.com/file/d/1i7MwmIsA5acsaX1GmkjpUP-_JebVM4_4/view?usp=sharing](https://drive.google.com/file/d/1i7MwmIsA5acsaX1GmkjpUP-_JebVM4_4/view?usp=sharing)

Then start speaking to the mic to test.

---

# Discussion

1. Before coding, setup API token from [AssemblyAI](https://app.assemblyai.com/).
2. Coding proper: Set up `PyAudio` library. This opens up the stream from the microphone, and setups the configurations for the audio stream.
    
    ```bash
    import pyaudio
     
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
    ```
    
3. Connect to AssemblyAI API that handles the transcription using `Websockets`.
    
    ```bash
    # the AssemblyAI endpoint we're going to hit
    URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"
    
    ...
    async with websockets.connect(
           URL,
           extra_headers=(("Authorization", auth_key),),
           ping_interval=5,
           ping_timeout=20
       ) 
    ...
    ```
    

1. Create asynchronous functions for sending and receiving audio data.
    
    ```bash
    async def send_receive():
    ...
    
    	#Sending Function
    	async def send():
    	...
    	
    	#Receving Function
    	async def receive():
    	...
    ```
    

1. Running the function
    
    ```bash
    asyncio.run(send_receive())
    ```
    

---

# References

[AssemblyAI Tutorial](https://www.assemblyai.com/blog/real-time-speech-recognition-with-python/)

[AssemblyAI Video](https://www.youtube.com/watch?v=5LJFK7eOC20)

[Github Repository](https://github.com/misraturp/Real-time-transcription-from-microphone)