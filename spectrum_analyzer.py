import math
import librosa
import matplotlib.pyplot as plt
import numpy as np

y, sr = librosa.load(r"your_audio.mp3", sr=None)
N = 1024  #frame size

columns = []
brightness = []
times = []

for start in range(0, len(y) - N, N):
    frame = y[start : start + N]
    spectrum = np.fft.rfft(frame)
    linear_mags = [abs(c) for c in spectrum]
    magnitudes = [20 * math.log10(m+ 1e-10) for m in linear_mags]
    columns.append(magnitudes)

    weighted_total = 0
    mag_total = 0

    for k in range(len(linear_mags)):
        mag_k = linear_mags[k]
        freq_k = k * sr / N
        weighted_total += freq_k * mag_k
        mag_total += mag_k
    if mag_total == 0:
        centroid = 0
    else: 
        centroid = weighted_total / mag_total     
    brightness.append(centroid)
    times.append(start / sr)

duration = len(y) / sr
nyquist = sr / 2

image = list(zip(*columns))


plt.imshow(image, origin="lower", aspect="auto", cmap="magma", extent=[0, duration, 0, nyquist])
plt.plot(times, brightness, color="cyan", linewidth=1, label="Spectral centroid (brightness)")
plt.legend()
plt.xlabel("Time (seconds)")
plt.ylabel("Frequency (Hz)")
plt.colorbar(label="Magnitude")
plt.show()