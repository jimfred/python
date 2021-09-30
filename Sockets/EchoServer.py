# Echo server program
import time
import socket

HOST = ''  # Symbolic name meaning all available interfaces
PORT = 50007  # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))

print(f'Listening on port {PORT}')
while True:
    s.listen(1)
    conn, addr = s.accept()
    print(f'Connected, addr {addr}')
    rx_all = bytearray(b'')
    while True:
        rx = conn.recv(1024)
        rx_all += bytearray(rx)
        rx_str = rx_all.decode()
        print(f'{rx_str}')
        if 0 == len(rx) or b'.'[-1] == rx[-1]:
            break
    # Prepare response.
    tx_str = rx_str.upper()
    print(f'Got {rx_str} sending {tx_str}')

    tx_all = tx_str.encode()

    # Send response.
    conn.send(tx_all)
    time.sleep(1)

    conn.close()
