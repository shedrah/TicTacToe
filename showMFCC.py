import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np


audio_file = "stp.wav"
signal, sr = librosa.load(audio_file)
signal.shape

mfccs = librosa.feature.mfcc(signal, n_mfcc=13, sr=sr)

mfccs.shape
print(mfccs)
fig=plt.figure(figsize=(25,10))
librosa.display.specshow(mfccs,
                         x_axis="time",
                         sr=sr)
fig.gca().set_xlabel("Czas [s]", fontsize=17)
fig.gca().set_ylabel("Współczynniki", fontsize=17)
plt.colorbar(format="%+2f")

# plt.show()