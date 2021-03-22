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


def find_next_minus_one(head, v_raw):
    for i in range(head, v_raw.size):
        if v_raw[i] == -1:
            return i

    return None


def find_next_non_minus_one(head, v_raw):
    for i in range(head+1, v_raw.size):
        if v_raw[i] != -1:
            return i

    return None  # this line should not be run at any time after modifying the last elements to non -1


def perform_inerpolation(head, back, v_raw):
    prev_value = v_raw[back-1]
    curr_value = v_raw[head]
    increment = (curr_value - prev_value) / (head - (back-1))

    for i in range(back, head):
        v_raw[i] = v_raw[i-1] + increment


def v_linear_interpolation(v_raw):
    # find index of first non -1 data
    first_value_index = 0
    for v in v_raw:
        if v == -1:
            first_value_index += 1
        else:
            break
    # modify first -1's to value of first non -1
    for i in range(first_value_index):
        v_raw[i] = v_raw[first_value_index]

    # find index of last non -1 data
    last_value_index = v_raw.size - 1
    for i in range(v_raw.size - 1, 0, -1):
        if v_raw[i] == -1:
            last_value_index -= 1
        else:
            break

    # modify last -1's to value of last non -1
    for i in range(last_value_index + 1, v_raw.size):
        v_raw[i] = v_raw[last_value_index]

    head = 0
    back = 0
    while True:
        back = find_next_minus_one(head, v_raw)
        if back is None:
            break
        head = find_next_non_minus_one(head, v_raw)
        perform_inerpolation(head, back, v_raw)

    return v_raw


def caculate_accelarion_from_speed(v_interpolation, t_raw):
    acl = np.zeros(v_interpolation.shape)
    acl[0] = 0
    for i in range(1, acl.size):
        acl[i] = (v_interpolation[i] - v_interpolation[i-1])/((t_raw[i]-t_raw[i-1]) * 3.6)

    return acl


def main():
    global Fs, w_c

    taps = sig.firwin(N, w_c)  # by default window='hamming'
    path = eg.fileopenbox()
    accel = np.loadtxt(path, delimiter=',')
    t_raw = accel[:, 0]
    x_raw = accel[:, 1] * STANDARD_GRAVITY
    y_raw = accel[:, 2] * STANDARD_GRAVITY
    z_raw = accel[:, 3] * STANDARD_GRAVITY
    v_raw = accel[:, 4]

    v_interpolation = v_linear_interpolation(v_raw)
    accel_dv2dt = caculate_accelarion_from_speed(v_interpolation, t_raw)

    Fs = 1 / np.average(t_raw[1:] - t_raw[:-1])

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
    '''
    v1 = avg_filter(5, x_raw)
    v2 = avg_filter(8, x_raw)
    v3 = avg_filter(10, x_raw)
    '''
    v4 = avg_filter(15, x_raw)
    v5 = avg_filter(22, x_raw)
    accel_dv2dt_avg_22 = avg_filter(15, accel_dv2dt)

    t = np.arange(0, x1.shape[0] / Fs, 1/Fs)

    fig, axs = plt.subplots(2)

    axs[0].plot(t, x_raw, label='raw')

    # axs[0].plot(t, x1, label='X1-5')
    # axs[0].plot(t, x2, label='X2-10')
    # axs[0].plot(t, x3, label='X3-20')
    # axs[0].plot(t, x4, label='X4-40')
    # axs[0].plot(t, x5, label='X5-80')

    # axs[0].plot(t, v1, label='V1-5')
    # axs[0].plot(t, v2, label='V2-8')
    # axs[0].plot(t, v3, label='V3-10')
    # axs[0].plot(t, v4, label='V4-15')
    # axs[0].plot(t, v5, label='V5-22')
    axs[0].plot(t, accel_dv2dt, label='dv/dt')
    axs[0].plot(t, accel_dv2dt_avg_22, label='dv/dt filt')
    axs[0].legend()

    axs[1].plot(t, v_interpolation, label='speed')

    axs[1].legend()

    plt.show()


if __name__ == '__main__':
    main()