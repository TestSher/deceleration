import easygui as eg
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig

# standard gravity m/s^2
STANDARD_GRAVITY = 9.80665
# design FIR filter
# Sampling Frequency
Fs = 50
# filter order
N = 40
# cutoff frequency
fc = 3
# normalized frequency
w_c = 2 * fc / Fs


def avg_filter(avg_len, raw_samples):
    avg_lst = [0] * avg_len
    result = [0] * len(raw_samples)

    avg_sum = 0.0
    indx = 0
    result_indx = 0

    for sample in raw_samples:
        weight_sample = sample / avg_len
        avg_sum = avg_sum - avg_lst[indx] + weight_sample
        avg_lst[indx] = weight_sample

        result[result_indx] = avg_sum
        result_indx += 1

        indx += 1
        if indx >= avg_len:
            indx = 0
    return result


def main():
    global Fs, w_c

    taps = sig.firwin(N, w_c)  # by default window='hamming'
    path = eg.fileopenbox()
    accel = np.loadtxt(path, delimiter=',', skiprows=1) * STANDARD_GRAVITY
    x_raw = accel[:, 0]
    y_raw = accel[:, 1]
    z_raw = accel[:, 2]

    Fs = 20
    if '20d' in path:
        Fs = 50

    w_c = 2 * fc / Fs
    taps1 = sig.firwin(5, w_c)  # by default window='hamming'
    taps2 = sig.firwin(10, w_c)  # by default window='hamming'
    taps3 = sig.firwin(20, w_c)  # by default window='hamming'
    taps4 = sig.firwin(40, w_c)  # by default window='hamming'
    taps5 = sig.firwin(80, w_c)  # by default window='hamming'

    x1 = sig.lfilter(taps1, [1.0], x_raw)
    x2 = sig.lfilter(taps2, [1.0], x_raw)
    x3 = sig.lfilter(taps3, [1.0], x_raw)
    x4 = sig.lfilter(taps4, [1.0], x_raw)
    x5 = sig.lfilter(taps5, [1.0], x_raw)

    # starts with avg of 5 last points
    # and adds 50% each time
    v1 = avg_filter(5, x_raw)
    v2 = avg_filter(8, x_raw)
    v3 = avg_filter(10, x_raw)
    v4 = avg_filter(15, x_raw)
    v5 = avg_filter(22, x_raw)

    t = np.arange(0, x1.shape[0] / Fs, 1/Fs)

    plt.plot(t, x_raw, label='raw')

    plt.plot(t, x1, label='X1')
    plt.plot(t, x2, label='X2')
    plt.plot(t, x3, label='X3')
    plt.plot(t, x4, label='X4')
    plt.plot(t, x5, label='X5')

    plt.plot(t, v1, label='V1')
    plt.plot(t, v2, label='V2')
    plt.plot(t, v3, label='V3')
    plt.plot(t, v4, label='V4')
    plt.plot(t, v5, label='V5')

    plt.legend()

    plt.show()


if __name__ == '__main__':
    main()