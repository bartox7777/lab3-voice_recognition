import warnings

warnings.simplefilter("ignore")

import scipy.io.wavfile as wav
import scipy
import numpy as np
import sys, os
from scipy.signal import medfilt

# rozpoznanie płci osoby mówiącej metodą cepstralną

# err_matrix = [[0, 0], [0, 0]]

try:
    file = sys.argv[1]
except:
    print("Podaj nazwę pliku w pierwszym argumencie")
    exit(-1)

# for file in os.listdir("train"):
# fs, data = wav.read(f"train/{file}") # wczytanie pliku
fs, data = wav.read(file) # wczytanie pliku

if len(data.shape) > 1:
    data = data[:, 0] # jeśli plik jest stereo, to bierzemy tylko jeden kanał

try:
    data = medfilt(data, 3) # filtr medianowy
except:
    pass

freqs = np.fft.fftfreq(len(data), 1/fs)  # obliczenie częstotliwości

window = scipy.signal.windows.flattop(len(data)) # okno flattopa

data = data * window # zastosowanie okna

spectrum = np.fft.fft(data) # obliczenie spektrum

log_spectrum = np.log(np.abs(spectrum)) # logarytmowanie

cepstrum = np.abs(np.fft.fft(log_spectrum)) # obliczenie cepstrum

cepstrum_freqs = np.fft.fftfreq(len(log_spectrum), (freqs[1]-freqs[0])) # obliczenie częstotliwości cepstrum

human_freqs_range = (50, 300)

limited_cepstrum_freqs = (cepstrum_freqs > 1/human_freqs_range[1]) & (cepstrum_freqs <= 1/human_freqs_range[0]) # ograniczenie zakresu częstotliwości

peak_idx = np.argmax(cepstrum[limited_cepstrum_freqs]) # znalezienie indeksu największej wartości w ograniczonym zakresie

peak_freq = 1/cepstrum_freqs[limited_cepstrum_freqs][peak_idx] # znalezienie częstotliwości odpowiadającej indeksowi

real_gender = file.split(".")[0][-1]

if peak_freq <= 170:
    detected_gender = "M"
else:
    detected_gender = "K"

print(detected_gender)

    # if real_gender == "M":
    #     if detected_gender == "M":
    #         err_matrix[0][0] += 1
    #     else:
    #         err_matrix[0][1] += 1
    # else:
    #     if detected_gender == "K":
    #         err_matrix[1][1] += 1
    #     else:
    #         err_matrix[1][0] += 1

# print(err_matrix)

