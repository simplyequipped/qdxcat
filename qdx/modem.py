import os, subprocess, threading, time
from subprocess import PIPE


class MiniModem:
    RX = 'rx'
    TX = 'tx'
    MODES = [RX, TX]

    def __init__(self, mode, alsa_dev, baudrate=300, start=True):

        if mode in MiniModem.MODES:
            self.mode = mode
        else:
            raise Exception('Unknown mode \'' + mode + '\'')

        self.alsa_dev = alsa_dev
        self.baudrate = baudrate
        self.process = None
        self.active = False
        self.execpath = subprocess.check_output(['which', 'minimodem']).decode('utf-8').strip()

        self.shellcmd = [
            self.execpath,
            '--' + self.mode,
            '--quiet',
            '--alsa=' + self.alsa_dev,
            str(self.baudrate)
        ]

        if start:
            self.start()

    def start(self):
        if not self.active:
            self.process = subprocess.Popen(self.shellcmd, stdin=PIPE, stdout=PIPE)
            self.active = True

    def stop(self):
        self.active = False

        self.process.terminate()
        self.process.communicate()
        if self.process.poll() == None:
            self.process.kill()




#TODO add alsa_dev_in and alsa_dev_out

class Modem:
    RX      = 'rx'
    TX      = 'tx'
    RXTX    = 'rx/tx'
    MODES = [RX, TX, RXTX]

    @staticmethod
    def find_alsa_device(search_str='QDX'):
        alsa_dev = None
        alsa_devs = subprocess.check_output(['arecord', '-l']).decode('utf-8')
        alsa_devs = alsa_devs.split('\n')

        for line in alsa_devs:
            if search_str in line:
                start = 'card'
                end = ':'
                start_index = line.find(start) + len(start)
                end_index = line.find(end, start_index)
                card = line[start_index:end_index].strip()

                start = 'device'
                end = ':'
                start_index = line.find(start) + len(start)
                end_index = line.find(end, start_index)
                device = line[start_index:end_index].strip()

                alsa_dev = card + ',' + device
                break

        return alsa_dev

    def __init__(self, alsa_dev_in, alsa_dev_out=None, baudrate=300, mode='rx/tx', start=True):
        self.baudrate = baudrate
        self.alsa_dev_in = alsa_dev_in
        self.alsa_dev_out = alsa_dev_out
        self.rx = None
        self.tx = None
        self.active = False

        if mode in Modem.MODES:
            self.mode = mode
        else:
            raise Exception('Unknown mode \'' + mode + '\'')

        if self.alsa_dev_out == None:
            self.alsa_dev_out = self.alsa_dev_in

        if self.mode in [Modem.RXTX, Modem.RX]:
            self.rx = MiniModem(MiniModem.RX, self.alsa_dev_in, baudrate=self.baudrate, start=False)

        if self.mode in [Modem.RXTX, Modem.TX]:
            self.tx = MiniModem(MiniModem.TX, self.alsa_dev_out, baudrate=self.baudrate, start=False)

        if start:
            self.start()

    def start(self):
        if self.rx:
            self.rx.start()
        if self.tx:
            self.tx.start()

        self.active = True

        self._job_thread = threading.Thread(target=self._job_loop)
        self._job_thread.daemon = True
        self._job_thread.start()

    def stop(self):
        self.active = False

        if self.tx:
            self.tx.stop()
        if self.rx:
            self.rx.stop()

    def send(self, data):
        if not self.tx:
            return None

        if not type(data) is bytes:
            data = data.encode('utf-8')

        self.tx.process.stdin.write(data)

    def receive(self, size=-1):
        if not self.rx:
            return None

        return self.rx.process.stdout.read(size).decode('utf-8')

    def register_rx_callback(self, func):
        pass

    def _job_loop(self):
        while self.active:
            if self.rx:
                data = ''

                try:
                    data = self.receive()
                except UnicodeDecodeError as e:
                    #TODO handle error
                    pass

                if len(data):
                    print(data)

            time.sleep(1)


if __name__ == '__main__':
    alsa = input('Enter alsa device (card,device): ')
    modem = Modem(alsadev = alsa, mode=Modem.RX)
    print('Modem active')






