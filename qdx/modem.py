import os, threading, time, subprocess
import alsaaudio


class Modem:

    RX = 0x0
    TX = 0x1

    def __init__(self):

        self.fifo = '/tmp/fifo.wav'
        if not os.path.exists(self.fifo):
            os.mkfifo(self.fifo)

        self.tx_buffer = ''
        self.modem = None
        self.active = True
        self.mode = self.RX

        # TODO rx/tx threads or modem/radio threads?
        self._tx_event = threading.Event()
        self._shutdown_event = threading.Event()

    def tx(self, data):
        self.tx_buffer += data
        self.tx_event.set()
        # wait for rx to finish
        while self.mode == self.RX:
            time.sleep(0.1)


        self.mode = self.RX
        self.tx_event.clear()

    def rx(self):
        self._modem_rx_thread = threading.Thread(target=self._modem_rx)
        self._radio_rx_thread = threading.Thread(target=self._radio_rx)
        self._modem_rx_thread.start()
        self._radio_rx_thread.start()
            # open minimodem reading from fifo
            # open audio stream writing to fifo
            if self.tx_event.is_set():
                self.mode = self.TX
                self.tx_event.wait()
    
    def _tx(self):
            # TODO update min buffer size to tx
        while self.active and len(self.tx_buffer):
            self.__radio_tx()
            self.__modem_tx()

    def _radio_rx(self):
        # configure audio device
        # rx loop
        if self._shutdown_event.is_set():
            break

    def _radio_tx(self):
        if self._shutdown_event.is_set():
            break

    def _modem_rx(self):
        if self._shutdown_event.is_set():
            break

    def _modem_tx(self):
        if self._shutdown_event.is_set():
            break

    def end(self):
        self._shutdown_event.set()



# open read only
os.open(fifo, flags=os.O_NONBLOCK | os.O_RDONLY)
os.open(fifo, flags=os.O_NONBLOCK | os.O_WRONLY)

print(alsaaudio.pcms())
