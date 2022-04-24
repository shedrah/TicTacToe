import tensorflow.keras as keras
import numpy as np
import librosa
MODEL_PATH = "model.h5"
NUM_SAMPLES_TO_CONSIDER = 22050  # 1 sec

"""
Module that uses trained model to get
This is based on video series: https://www.youtube.com/watch?v=CA0PQS1Rj_4&list=PL-wATfeyAMNpCRQkKgtOZU_ykXc63oyzp
by Valerio Velardo
"""

class _Keyword_Spotting_Service:

    model = None
    mappings = [
        "down",
        "go",
        "left",
        "right",
        "stop",
        "up"
    ]
    instance = None

    def predict(self, file_path):

        # extract MFCCs
        MFCCs = self.preprocess(file_path)
        # convert 2d MFCCs array into 4d array
        MFCCs = MFCCs[np.newaxis, ..., np.newaxis]
        # make prediction
        predictions = self.model.predict(MFCCs)
        predicted_index = np.argmax(predictions)
        predicted_keyword = self.mappings[predicted_index]
        print(f"Predicted word: {predicted_keyword}")
        return predicted_keyword

    def preprocess(self, file_path, n_mfcc=13, n_fft=2048, hop_length=512):

        # load audio file
        signal, sr = librosa.load(file_path)
        # ensure 1 sec length
        if len(signal) > NUM_SAMPLES_TO_CONSIDER:
            signal = signal[:NUM_SAMPLES_TO_CONSIDER]
        # extract MFCCs
        MFCCs = librosa.feature.mfcc(signal, n_mfcc=n_mfcc, n_fft=n_fft, hop_length=hop_length)

        return MFCCs.T


def Keyword_Spotting_Service():

    # singleton
    if _Keyword_Spotting_Service.instance is None:
        _Keyword_Spotting_Service.instance = _Keyword_Spotting_Service()
        _Keyword_Spotting_Service.model = keras.models.load_model(MODEL_PATH)

    return _Keyword_Spotting_Service.instance


if __name__ == "__main__":

    kss = Keyword_Spotting_Service()
    keyword = kss.predict("demo.wav")
    print(f"Predicted word: {keyword}")
