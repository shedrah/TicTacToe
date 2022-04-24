import librosa
import os
import json

"""
Module that prepares dataset (extracts MFCC) to be able to be processed by neural network
This is based on video series: https://www.youtube.com/watch?v=CA0PQS1Rj_4&list=PL-wATfeyAMNpCRQkKgtOZU_ykXc63oyzp
by Valerio Velardo
"""

DATASET_PATH = "dataset"  # folder
JSON_PATH = "data.json"  # folder
SAMPLES = 22050  # 1 sec worth of sound, based on librosa data loading


def prepare_dataset(dataset_path, json_path, n_mfcc=13, hop_length=512, number_fft=2048):  # hop_length - size of segment, n_fft - size of window
    data = {
        "mappings": [],  # "left", "right", "up", down", "stop", "go"
        "labels": [],  # target outputs
        "MFCCs": [],  # inputs
        "files": []  # "dataset/left/1.wav"
    }
    # looping through all sound directories
    for i, (dirpath, dirnames, filenames) in enumerate(os.walk(dataset_path)):
        if dirpath is not dataset_path:  # browsing subdirectories
            #  update mappings
            category = dirpath.split("/")[-1]  # [dataset, left, right etc]
            data["mappings"].append(category)
            print(f"Processing {category}")
            #  looping through all sound files
            for f in filenames:
                # get file path
                file_path = os.path.join(dirpath, f)
                # librosa loading
                signal, sr = librosa.load(file_path)
                # condition for audiofile 1 sec length
                if len(signal) >= SAMPLES:
                    # shaving files longer than 1 sec
                    signal = signal[:SAMPLES]
                    # extract MFCCs, result is np.array
                    MFCCs = librosa.feature.mfcc(signal, n_mfcc=n_mfcc, hop_length=hop_length, n_fft=number_fft)
                    # store data
                    data["labels"].append(i-1)
                    data["MFCCs"].append(MFCCs.T.tolist())
                    data["files"].append(file_path)
                    print(f"{file_path}: {i-1}")
    # store in json file
    with open(json_path, "w") as fp:
        json.dump(data, fp, indent=4)


if __name__ == "__main__":
    prepare_dataset(DATASET_PATH, JSON_PATH)
