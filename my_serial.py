#!/usr/bin/env python3
#3.0{30/112020}


import time
import serial

MAX_RECEIVE = 25
STATE0 = 0
STATE1 = 1
state = STATE0

rx_buff = b''
ch_counter = 0


def parse_message(msg):
    lst = msg.split(',')
    result = []
    for num in lst:
        result.append(float(num))
    return result


def legal_char(rd):
    if rd in b'.,-$':          # == b'.' or rd == b',' or rd == b'$':
        return True
    if rd >= b'0' and rd <= b'9':
        return True
    return False


# return None or '#3.21,4.56,2.22$'
def get_message(ser):
    global rx_buff, state, ch_counter

    while ser.in_waiting > 0:
        rd = ser.read()
        # print(rd)
        if state == STATE0:
            rx_buff = b''
            ch_counter = 0
            if rd == b'#':
                rx_buff += rd
                ch_counter += 1
                state = STATE1
        elif state == STATE1:
            ch_counter += 1
            if ch_counter >= MAX_RECEIVE:
                state = STATE0
                return None
            if not legal_char(rd):
                state = STATE0
                return None

            if rd == b'$':
                rx_buff += rd
                state = STATE0
                return rx_buff.decode()

            rx_buff += rd

    return None


def my_init_serial():
    ser = serial.Serial('COM3', 9600) #/dev/ttyACM0
    # ser.flush()
    ser.reset_input_buffer()
    ser.reset_output_buffer()

    return ser


def main():

    ser = my_init_serial()
    while True:
        msg = get_message(ser)
        if msg != None:
            msg1 = msg[1:-1]
            result = parse_message(msg1)
            print(result)

        time.sleep(0.005)


if __name__ == '__main__':
    main()
