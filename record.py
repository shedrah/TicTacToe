import pyaudio
import wave
from array import array


def record_word():
    FORMAT=pyaudio.paInt16
    CHANNELS=2
    RATE= 44100
    CHUNK=1024
    RECORD_SECONDS=2
    FILE_NAME="demo.wav"
    audio = pyaudio.PyAudio()  # instantiate the pyaudio

    # recording prerequisites
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    #start recording
    ready = True
    frames=[]

    for i in range(0,int(RATE/CHUNK*RECORD_SECONDS)):
        data = stream.read(CHUNK)
        data_chunk = array('h', data)
        vol = max(data_chunk)
        if(vol>=200):
            print("something said")
            frames.append(data)
        else:
            print("nothing")
        print("\n")

    # end of recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
    # write to file
    wavfile=wave.open(FILE_NAME,'wb')
    wavfile.setnchannels(CHANNELS)
    wavfile.setsampwidth(audio.get_sample_size(FORMAT))
    wavfile.setframerate(RATE)
    wavfile.writeframes(b''.join(frames))
    wavfile.close()
    ready = False


if __name__ == "__main__":
    record_word()
