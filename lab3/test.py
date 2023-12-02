



import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import scipy
import numpy as np
import os
from scipy.signal import medfilt
from scipy.signal import wiener
from scipy.signal import butter

# rozpoznanie płci osoby mówiącej metodą cepstralną



good = 0
bad = 0

M = []
K = []

for file in os.listdir("train"):
    fs, data = wav.read(f'train/{file}') # wczytanie pliku

    if len(data.shape) > 1:
        data = data[:, 0] # jeśli plik jest stereo, to bierzemy tylko jeden kanał
    
    try:    
        data = medfilt(data, 3)
    except:
        pass
        
    freqs = np.fft.fftfreq(len(data), 1/fs)  # obliczenie częstotliwości
        
    window = scipy.signal.windows.blackman(len(data)) # okno blackmana

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
    
    if real_gender == detected_gender:
        good += 1
    else:
        bad += 1
        
    if real_gender == "K":
        K.append(peak_freq)
    else:
        M.append(peak_freq)
    
    # print(f"{file}: {peak_freq}") # wypisanie częstotliwości
    
# print(f"mediana, srednia K: {np.median(K)} {np.mean(K)}")
# print(f"mediana, srednia M: {np.median(M)} {np.mean(M)}")
    

print(good)
print(bad)

##########

# import scipy.io.wavfile as wav
# import matplotlib.pyplot as plt
# import scipy
# import numpy as np
# import os


# K = []
# M = []

# for file in os.listdir("train"):
#     fs, dataB = wav.read(f'train/{file}')
#     if len(dataB.shape) > 1:
#         dataB = dataB[:, 0] 
    
#     for i in range(3):
#         data = dataB[i*len(dataB)//3:(i+1)*len(dataB)//3]
#         # freqs = np.linspace(0, fs, len(data), endpoint=False)
#         freqs = np.fft.fftfreq(len(data), 1/fs)
            
#         window = scipy.signal.windows.blackman(len(data))

#         data = data * window

#         spectrum = (abs(np.fft.fft(data))[0:int(len(data)/2)])/fs

#         num = 5
#         spectrumCpy = spectrum.copy()
#         for i in range(2, num):
#             downsampled = spectrum[::i].copy()
#             spectrumCpy = spectrumCpy[:len(downsampled)]
#             spectrumCpy = spectrumCpy * downsampled
        
#         print(freqs[np.argmax(spectrumCpy)])
            
        # gender = file.split(".")[0][-1]
        # if gender == "K":
        #     K.append(freqs[np.argmax(spectrumCpy)])
        # else:
        #     M.append(freqs[np.argmax(spectrumCpy)])

# print(K)
# print(M)
# T = 5
# fs, dataB = wav.read(f'train/015_K.wav')
# if len(dataB.shape) > 1:
#     dataB = dataB[:, 0] 

# for i in range(T):
#     data = dataB[i*len(dataB)//T:(i+1)*len(dataB)//T]
#     # freqs = np.linspace(0, fs, len(data), endpoint=False)
#     freqs = np.fft.fftfreq(len(data), 1/fs)
        
#     window = scipy.signal.windows.blackman(len(data))

#     data = data * window

#     # spectrum = (abs(np.fft.fft(data))[0:int(len(data)/2)])/fs
#     spectrum = abs(np.fft.fft(data))/fs

#     num = 5
#     spectrumCpy = spectrum.copy()
#     for i in range(2, num):
#         downsampled = spectrum[::i].copy()
#         spectrumCpy = spectrumCpy[:len(downsampled)]
#         spectrumCpy = spectrumCpy * downsampled
    
#     print(freqs[np.argmax(spectrumCpy)])

# fs, data = wav.read(f'train/015_K.wav')
# if len(data.shape) > 1:
#     data = data[:, 0]
    
# # plt.plot(data)
# # plt.show()
    
# freqs = np.fft.fftfreq(len(data), 1/fs)
    
# window = scipy.signal.windows.blackman(len(data))

# data = data * window

# # plt.plot(data)
# # plt.show()

# spectrum = (np.abs(np.fft.fft(data))) / fs

# plt.plot(spectrum)
# plt.xscale("log")
# plt.show()

# num = 5
# spectrumCpy = spectrum.copy()
# for i in range(2, num):
#     downsampled = spectrum[::i].copy()
#     spectrumCpy = spectrumCpy[:len(downsampled)]
#     spectrumCpy = spectrumCpy * downsampled
    
# human_freqs_range = (50, 300)

# freqs = freqs[:len(spectrumCpy)]

# limited_cepstrum_freqs = (freqs > 1/human_freqs_range[1]) & (freqs <= 1/human_freqs_range[0]) # ograniczenie zakresu częstotliwości



# print(spectrumCpy[limited_cepstrum_freqs])

# peak_idx = np.argmax(spectrumCpy[limited_cepstrum_freqs]) # znalezienie indeksu największej wartości w ograniczonym zakresie

# peak_freq = 1/spectrumCpy[limited_cepstrum_freqs][peak_idx] # znalezienie częstotliwości odpowiadającej indeksowi

# print(peak_freq)

# print(freqs)
# print(np.argmax(spectrumCpy))
# print(freqs[np.argmax(spectrumCpy)])


# freqs = np.linspace(0, fs, len(data), endpoint=False)
# plt.stem(freqs, spectrum, ".")
# plt.plot(spectrum)
# plt.xscale("log")
# plt.show()

# plt.plot(spectrum/fs)
# plt.xscale("log")
# plt.show()

# reduced versions of spectrum
# reduced_spectrums = []

# print(len(reduced_spectrums))

# min_len = len(reduced_spectrums[-1])
# hps = reduced_spectrums[-1]
# for i in range(len(reduced_spectrums)-2, -1, -1):
#     hps = hps * reduced_spectrums[i][:min_len]

# for i in range(2, num):
    

# plt.plot(hps)
# stem(freqs[:len(hps)], hps, '-*')
# plt.xscale("log")
# plt.show()

# stem(freqs[:len(hps)], hps, '-*')
# plt.xscale("log")
# plt.show()

# print(freqs[np.argmax(hps)])

