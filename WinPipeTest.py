'''
Start a server process and a client process that talk over a named pipe.
The client sends commands to the server and the server responds with an echoed variant of the command.
Used to test client+server here or client here with server elsewhere.
'''

import multiprocessing
import time
import pywintypes
import win32file
import win32pipe
import winerror

pipe_name = r'\\.\pipe\WinPipeTest'  # used by both server and client.
pipe_max_msg_size = 20


def s():
    me = 'server:'
    print(f"{me} start")
    pipe = win32pipe.CreateNamedPipe(
        pipe_name,
        win32pipe.PIPE_ACCESS_DUPLEX,
        win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
        1,  # nMaxInstances
        pipe_max_msg_size,
        pipe_max_msg_size,
        0,  # nDefaultTimeOut
        None  # PySECURITY_ATTRIBUTES
    )
    try:
        print(f"{me} waiting for client")
        win32pipe.ConnectNamedPipe(pipe, None)
        print(f"{me} got client")

        while True:  # Normally exits via exception when client closes pipe.
            (err, b) = win32file.ReadFile(pipe, pipe_max_msg_size)
            assert(err == winerror.S_OK)
            rx_cmd = b.decode()
            tx_rsp = rx_cmd.upper()  # change the cmd and echo.
            print(f"{me} rx {rx_cmd}, tx {tx_rsp}")
            (err, qty) = win32file.WriteFile(pipe, str.encode(tx_rsp))
            assert(err == winerror.S_OK)
    except pywintypes.error as e:
        if e.args[0] == winerror.ERROR_FILE_NOT_FOUND:
            print(me, e.args[0], e)
        elif e.args[0] == winerror.ERROR_BROKEN_PIPE:  # normal closure of pipe by client.
            print(me, 'pipe closed')
    except Exception as e:
        print(me, e)

    try:
        win32file.CloseHandle(pipe)
    except Exception as e:
        print(me, 'Closed handle', e)
    print(me, "done")


def c():
    me = '    client:'
    print(f"{me} start")

    try:
        handle = win32file.CreateFile(
            pipe_name,
            win32file.GENERIC_READ | win32file.GENERIC_WRITE,
            0,  # shareMode
            None,  # PySECURITY_ATTRIBUTES
            win32file.OPEN_EXISTING,
            0,  # flagsAndAttributes
            None
        )
        res = win32pipe.SetNamedPipeHandleState(handle, win32pipe.PIPE_READMODE_MESSAGE, None, None)
        if res == 0:
            print(f"{me} SetNamedPipeHandleState return code: {res}")

        time.sleep(1)

        for i in range(5):
            command = f'cmd{i}'
            print(f"{me} write {command}")
            (err, qty) = win32file.WriteFile(handle, str.encode(command))
            assert(err == winerror.S_OK)
            (err, b) = win32file.ReadFile(handle, pipe_max_msg_size)
            assert(err == winerror.S_OK)
            rsp = b.decode()
            print(f"{me} got: {rsp}")
    except pywintypes.error as e:
        if e.args[0] == winerror.ERROR_FILE_NOT_FOUND:
            print(me, e.args[0], e)
        elif e.args[0] == winerror.ERROR_BROKEN_PIPE:
            print(me, 'pipe closed', e)
    except Exception as e:
        print(me, e)

    try:
        win32file.CloseHandle(handle)
    except Exception as e:
        print(me, 'Closed handle', e)
    print(f"{me} done")


if __name__ == '__main__':
    TEST_SERVER = 0  # turn off to test with other server..
    print("test start")
    cp = multiprocessing.Process(target=c)
    if TEST_SERVER:
        sp = multiprocessing.Process(target=s)
        sp.start()  # Start server process.
    cp.start()  # Start client process.
    print("test wait")
    if TEST_SERVER:
        sp.join()
    cp.join()
    print("test done")

