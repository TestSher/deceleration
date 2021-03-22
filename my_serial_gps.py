#!/usr/bin/env python3
#3.4{27/1/2021}


import time
import serial

MAX_RECEIVE = 48
STATE0 = 0
STATE1 = 1
state = STATE0

rx_buff = b''
ch_counter = 0


def parse_message(msg):
    lst = msg.split(',')
    #print(msg)
    return float(lst[7])
    '''
    result = []
    for num in lst:
        result.append(float(num))
    return result
    '''


def legal_char(rd):
    if rd in b'.,-GPVT$TMNK*':          # == b'.' or rd == b',' or rd == b'$':
        return True
    if rd >= b'0' and rd <= b'9':
        return True

    #print(f'{rd}')  #here
    return False


# return None or 'b'$GPVTG,360.0,T,348.7,M,000.0,N,000.0,K*43'
def get_message(ser):
    global rx_buff, state, ch_counter

    while ser.in_waiting > 0:
        rd = ser.read()
        #print(rd)
        if state == STATE0:
            rx_buff = b''
            ch_counter = 0
            if rd == b'T':
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

            if rd == b'K':
                rx_buff += rd
                #print(rx_buff)
                state = STATE0
                return rx_buff.decode()

            rx_buff += rd

    return None


def my_init_serial():
    ser = serial.Serial('/dev/ttyS0', 38400) #/dev/ttyACM0
    # ser.flush()
    ser.reset_input_buffer()
    ser.reset_output_buffer()

    return ser


def main():

    ser = my_init_serial()
    while True:
        msg = get_message(ser)
        if msg != None:
            #print(msg)
            msg1 = msg[1:-1]
            result = parse_message(msg1)
            print(result)

        time.sleep(0.005)


if __name__ == '__main__':
    main()