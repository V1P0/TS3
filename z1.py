import libscrc
import argparse

FLAG = '01111110'
frame_size = 64


def gen_crc(message):
    return bin(libscrc.crc8(bytes(message, 'utf-8')))[2:].zfill(8)


def slice_data(data):
    result = []
    while len(data) > 0:
        a = data[:frame_size]
        data = data[frame_size:]
        result.append(a)
    return result


def encode(data):
    sliced_data = slice_data(data)
    result = ""
    for frame in sliced_data:
        result += FLAG + (frame + gen_crc(frame)).replace('11111', '111110') + FLAG
    return result


def decode(data):
    sliced_data = data.split(FLAG)
    result = ""
    for i, frame in enumerate(sliced_data):
        if i % 2 == 0:
            continue
        frame = frame.replace('111110', '11111')
        message = frame[:-8]
        crc = frame[-8:]
        if crc != gen_crc(message):
            print("CRC error")
            exit(0)
        result += message
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-bs", "--frame_size", help="rozmiar bloku", default=64)
    parser.add_argument("-i", "--input", help="plik źródłowy", default="Z.txt")
    parser.add_argument("-o", "--output", help="plik wynikowy", default="W.txt")
    parser.add_argument("-m", "--mode", help="tryb działania", choices=['encode', 'decode'], default='encode')
    args = parser.parse_args()

    global frame_size
    frame_size = args.frame_size
    mode = args.mode
    with open(args.input, 'r') as input_file:
        data = input_file.readline()
        if mode == 'encode':
            data = encode(data)
        else:
            data = decode(data)

    with open(args.output, 'w') as output_file:
        output_file.write(data)


if __name__ == '__main__':
    main()
