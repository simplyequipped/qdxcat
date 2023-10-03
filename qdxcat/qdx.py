# MIT License
# 
# Copyright (c) 2022-2023 Simply Equipped
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

'''QRPLabs QDX transceiver CAT control.

QDX commands are based on the Kenwood TS-480 command set.

**Note:** QDX firmware v1.06 or above is required, due to a significant change in commands in v1.06. See the *Firmware* section of the [QRPLabs QDX webpage](http://qrp-labs.com/qdx) for upgrade instructions.
'''

__docformat__ = 'google'

import time
import serial
import threading

from serial.tools.list_ports import grep


class QDX:
    '''QDX transceiver control object.
    
    Attributes:
        command_map (dict): map of command strings to associated data
        settings (dict): map of commands and current local values
        COMMANDS (list): list of command strings
        GET_COMMANDS (list): list of command strings that support a *get* operation
        SET_COMMANDS (list): list of command strings that support a *set* operation
    '''
    
    # QDX CAT commands
    # Kenwood TS-480/TS-440 command set
    AUDIO_GAIN       = 'AG'
    '''Minimum firmware version: 1.03'''
    SIG_GEN_FREQ     = 'C2'
    '''Minimum firmware version: 1.03'''
    VFO_A            = 'FA'
    '''Minimum firmware version: 1.03'''
    VFO_B            = 'FB'
    '''Minimum firmware version: 1.03'''
    RX_VFO_MODE      = 'FR'
    '''Minimum firmware version: 1.03'''
    TX_VFO_MODE      = 'FT'
    '''Minimum firmware version: 1.03'''
    FILTER_BW        = 'FW'
    '''Minimum firmware version: 1.03'''
    RADIO_ID         = 'ID'
    '''Minimum firmware version: 1.03'''
    RADIO_INFO       = 'IF'
    '''Minimum firmware version: 1.03'''
    RADIO_INFO_DICT  = '_IF'
    '''Same as QDX.RADIO_INFO, parsed into a dictionary

    Dictionary structure:
    ```
    {
        'vfo_freq': int,
        'rit_offset': int,
        'rit': bool,
        'xit': bool,
        'memory_bank': int,
        'memory_channel': int,
        'tx': bool,
        'rx': bool,
        'mode': int,
        'rx_vfo': int,
        'scan': bool,
        'split': bool,
        'tone': int,
        'tone_number': int
    }
    ```
    '''
    OPERATING_MODE   = 'MD'
    '''Minimum firmware version: 1.03'''
    TXCO_FREQ        = 'Q0'
    '''Minimum firmware version: 1.03'''
    SIDEBAND         = 'Q1'
    '''Minimum firmware version: 1.03'''
    DEFAULT_FREQ     = 'Q2'
    '''Minimum firmware version: 1.03'''
    VOX_EN           = 'Q3'
    '''Minimum firmware version: 1.06'''
    TX_RISE          = 'Q4'
    '''Minimum firmware version: 1.06'''
    TX_FALL          = 'Q5'
    '''Minimum firmware version: 1.06'''
    CYCLE_MIN        = 'Q6'
    '''Minimum firmware version: 1.06'''
    SAMPLE_MIN       = 'Q7'
    '''Minimum firmware version: 1.06'''
    DISCARD          = 'Q8'
    '''Minimum firmware version: 1.06'''
    IQ_MODE          = 'Q9'
    '''Minimum firmware version: 1.06'''
    JAPAN_BAND_LIM   = 'QA'
    '''Minimum firmware version: 1.06'''
    CAT_TIMEOUT_EN   = 'QB'
    '''Minimum firmware version: 1.06'''
    CAT_TIMEOUT      = 'QC'
    '''Minimum firmware version: 1.06'''
    PTT_PORT_SERIAL  = 'QD'
    '''Minimum firmware version: 1.06'''
    VGA_PS2_MODE     = 'QE'
    '''Minimum firmware version: 1.06'''
    SERIAL1_BAUD     = 'QF'
    '''Minimum firmware version: 1.06'''
    SERIAL2_BAUD     = 'QG'
    '''Minimum firmware version: 1.06'''
    SERIAL3_BAUD     = 'QH'
    '''Minimum firmware version: 1.06'''
    NIGHT_MODE       = 'QI'
    '''Minimum firmware version: 1.06'''
    TX_SHIFT         = 'QJ'
    '''Minimum firmware version: 1.06'''
    NEG_RIT_OFFSET   = 'RD'
    '''Minimum firmware version: 1.03'''
    RIT_STATUS       = 'RT'
    '''Minimum firmware version: 1.03'''
    POS_RIT_OFFSET   = 'RU'
    '''Minimum firmware version: 1.03'''
    RX_MODE          = 'RX'
    '''Minimum firmware version: 1.03'''
    SPLIT_MODE       = 'SP'
    '''Minimum firmware version: 1.03'''
    TX_STATE         = 'TQ'
    '''Minimum firmware version: 1.03'''
    TX_MODE          = 'TX'
    '''Minimum firmware version: 1.03'''
    VERSION          = 'VN'
    '''Minimum firmware version: 1.05'''

    COMMANDS = [AUDIO_GAIN, SIG_GEN_FREQ, VFO_A, VFO_B, RX_VFO_MODE, TX_VFO_MODE, FILTER_BW, RADIO_ID, RADIO_INFO, RADIO_INFO_DICT, OPERATING_MODE,
        TXCO_FREQ, SIDEBAND, DEFAULT_FREQ, VOX_EN, TX_RISE, TX_FALL, CYCLE_MIN, SAMPLE_MIN, DISCARD, IQ_MODE, JAPAN_BAND_LIM, CAT_TIMEOUT_EN,
        CAT_TIMEOUT, PTT_PORT_SERIAL, VGA_PS2_MODE, SERIAL1_BAUD, SERIAL2_BAUD, SERIAL3_BAUD, NIGHT_MODE, TX_SHIFT, NEG_RIT_OFFSET, RIT_STATUS,
        POS_RIT_OFFSET, RX_MODE, SPLIT_MODE, TX_STATE, TX_MODE, VERSION]
    
    SET_COMMANDS = [AUDIO_GAIN, SIG_GEN_FREQ, VFO_A, VFO_B, RX_VFO_MODE, TX_VFO_MODE, OPERATING_MODE, TXCO_FREQ, SIDEBAND, DEFAULT_FREQ, VOX_EN,
        TX_RISE, TX_FALL, CYCLE_MIN, SAMPLE_MIN, DISCARD, IQ_MODE, JAPAN_BAND_LIM, CAT_TIMEOUT_EN, CAT_TIMEOUT, PTT_PORT_SERIAL, VGA_PS2_MODE,
        SERIAL1_BAUD, SERIAL2_BAUD, SERIAL3_BAUD, NIGHT_MODE, TX_SHIFT, NEG_RIT_OFFSET, POS_RIT_OFFSET, RX_MODE, SPLIT_MODE, TX_STATE, TX_MODE]

    GET_COMMANDS = [AUDIO_GAIN, SIG_GEN_FREQ, VFO_A, VFO_B, RX_VFO_MODE, TX_VFO_MODE, FILTER_BW, RADIO_ID, RADIO_INFO, RADIO_INFO_DICT, OPERATING_MODE,
        TXCO_FREQ, SIDEBAND, DEFAULT_FREQ, VOX_EN, TX_RISE, TX_FALL, CYCLE_MIN, SAMPLE_MIN, DISCARD, IQ_MODE, JAPAN_BAND_LIM, CAT_TIMEOUT_EN, CAT_TIMEOUT,
        PTT_PORT_SERIAL, VGA_PS2_MODE, SERIAL1_BAUD, SERIAL2_BAUD, SERIAL3_BAUD, NIGHT_MODE, TX_SHIFT, RIT_STATUS, SPLIT_MODE, TX_STATE, VERSION]

    def __init__(self, port=None, baudrate=9600, timeout=1, autodetect=True):
        '''Initialize QDX instance object.

        Args:
            port (str): Windows COM port (ex. 'COM42') or Unix serial device path (ex. '/dev/ttyACM0'), defaults to None
            baudrate (int): Serial port baudrate, defaults to 9600
            timeout (int): Serial port timeout in seconds, defaults to 1
            autodetect (bool): Whether to auto-detect QDX device serial port, defaults to True

        Returns:
            qdxcat.QDX: Constructed QDX object
        '''
        self.command_map = {
            'AG' : {'description': 'Audio Gain',          'unit': 'dB',       'options': None},
            'C2' : {'description': 'Signal Gen',          'unit': 'Hz',       'options': None},
            'FA' : {'description': 'VFO A',               'unit': 'Hz',       'options': None},
            'FB' : {'description': 'VFO B',               'unit': 'Hz',       'options': None},
            'FR' : {'description': 'RX VFO Mode',         'unit': '',         'options': {0:'VFO A', 1:'VFO B', 2:'Split'}},
            'FT' : {'description': 'TX VFO Mode',         'unit': '',         'options': {0:'VFO A', 1:'VFO B', 2:'Split'}},
            'FW' : {'description': 'Filter Bandwidth',    'unit': 'Hz',       'options': None},
            'ID' : {'description': 'Radio ID',            'unit': '',         'options': None},
            'IF' : {'description': 'Radio Info',          'unit': '',         'options': None},
            'MD' : {'description': 'Operating Mode',      'unit': '',         'options': {1:'LSB', 3:'USB'}},
            'Q0' : {'description': 'TXCO',                'unit': 'Hz',       'options': None},
            'Q1' : {'description': 'Sideband',            'unit': '',         'options': {0:'USB', 1:'LSB'}},
            'Q2' : {'description': 'Default Freq',        'unit': 'Hz',       'options': None},
            'Q3' : {'description': 'VOX',                 'unit': '',         'options': {0:'Disabled', 1:'Enabled'}},
            'Q4' : {'description': 'TX Rise',             'unit': '%',        'options': None},
            'Q5' : {'description': 'TX Fall',             'unit': '%',        'options': None},
            'Q6' : {'description': 'Cycle Min',           'unit': 'cycles',   'options': None},
            'Q7' : {'description': 'Sample Min',          'unit': 'samples',  'options': None},
            'Q8' : {'description': 'Discard',             'unit': 'cycles',   'options': None},
            'Q9' : {'description': 'IQ Mode',             'unit': '',         'options': {0:'Disabled', 1:'Enabled'}},
            'QA' : {'description': 'Japan Band Mode',     'unit': '',         'options': {0:'Disabled', 1:'Enabled'}},
            'QB' : {'description': 'CAT Timeout Enable',  'unit': '',         'options': {0:'Disabled', 1:'Enabled'}},
            'QC' : {'description': 'CAT Timeout',         'unit': 'sec',      'options': None},
            'QD' : {'description': 'PTT Port as Serial',  'unit': '',         'options': {0:'Disabled', 1:'Enabled'}},
            'QE' : {'description': 'VGA PS/2 Mode',       'unit': '',         'options': {0:'Disabled', 1:'Enabled'}},
            'QF' : {'description': 'Serial 1 Baud Rate',  'unit': 'baud',     'options': None},
            'QG' : {'description': 'Serial 2 Baud Rate',  'unit': 'baud',     'options': None},
            'QH' : {'description': 'Serial 3 Baud Rate',  'unit': 'baud',     'options': None},
            'QI' : {'description': 'Night Mode',          'unit': '',         'options': {0:'Disabled', 1:'Enabled'}},
            'QJ' : {'description': 'TX Shift',            'unit': 'mHz',      'options': None},
            'RD' : {'description': 'Neg RIT Offset',      'unit': 'Hz',       'options': None},
            'RT' : {'description': 'RIT',                 'unit': '',         'options': {0:'Disabled', 1:'Enabled'}},
            'RU' : {'description': 'Pos RIT Offset',      'unit': 'Hz',       'options': None},
            'RX' : {'description': 'RX',                  'unit': '',         'options': None},
            'SP' : {'description': 'Split Mode',          'unit': '',         'options': {0:'Disabled', 1:'Enabled'}},
            'TQ' : {'description': 'RX/TX State',         'unit': '',         'options': {0:'RX', 1:'TX'}},
            'TX' : {'description': 'TX',                  'unit': '',         'options': None},
            'VN' : {'description': 'Firmware Version',    'unit': '',         'options': None}
        }
        '''
        Map of commands to associated data.
        
        Dictionary structure:
        ```
        {
            'CMD' : {
                'description': str, command description
                'units': str, command units (empty string if not applicable)
                'options': dict or None, dictionary of command options and description strings (None if no applicable)
            },
            ...
        }
        ```
        '''

        self.settings = {}
        '''
        Local settings representation. Updated automatically when QDX.set() is called.
        
        Dictionary structure:
        ```
        {
            'CMD' : int,
            ...
        }
        ```
        '''
        
        self._settings_lock = threading.Lock()
        self._debug = False
        
        # serial port config
        self._port = None
        self._baudrate = baudrate
        self._timeout = timeout

        if port is not None:
            self.set_port(port, baudrate, timeout)
        elif autodetect:
            self.autodetect()

    def autodetect(self):
        '''Auto-detect QDX device serial port.'''
        # linux port description: 'QDX Transceiver'
        # windows port description: 'USB Serial Device (COMx)'

        # try linux description
        ports = list( serial.tools.list_ports.grep('QDX Transceiver') )

        if len(ports) == 0:
            # try windows description
            ports = list( serial.tools.list_ports.grep('USB Serial Device') )
            
        if len(ports) == 0:
            # no matching device description on linux or windows
            raise IOError('QDX device not found, check device connection or specifiy a serial port')

        #TODO check radio ID string format
        #TODO are there exceptions to handle when trying serial requests to unknown devices?
        # check for QDX radio ID (Kenwood TS-480 = 020)
        ports = [port for port in ports if self._serial_request(QDX.RADIO_ID, device = port.device) == '020']

        if len(ports) > 1:
            devices = ', '.join( [port.name for port in ports] )
            raise IOError('Multiple QDX devices found, try specifying a serial port: {}'.format(devices))
        
        self.set_port(ports[0].device)

    def set_port(self, port, baudrate=9600, timeout=1, sync=True):
        '''Set QDX device serial port.

        Args:
            port (str): Windows COM port (ex. 'COM42') or Unix serial device path (ex. '/dev/ttyACM0')
            baudrate (int): Serial port baudrate, defaults to 9600
            timeout (int): Serial port timeout in seconds, defaults to 1
            sync (bool): Whether to sync local settings to transceiver settings, defaults to True
        '''
        if port is None:
            return
            
        self._port = port
        self._baudrate = baudrate
        self._timeout = timeout

        if sync:
            # minimize delay at startup by using a thread
            thread = threading.Thread(target=self.sync_local_settings)
            thread.daemon = True
            thread.start()

    def get(self, cmd, update=False):
        '''Get command value.

        Args:
            cmd (str): Command to get value for
            update (bool): Update local settings from QDX settings if True, or use local settings if False, defaults to False

        Returns:
            int: Command value

        Raises:
            ValueError: Invalid QDX command
            ValueError: Command is not settable (not in QDX.SET_COMMANDS)
        '''
        if cmd not in QDX.COMMANDS:
            raise ValueError('Invalid QDX command: {}'.format(cmd))
            
        if cmd not in QDX.SET_COMMANDS:
            raise ValueError('Command is not gettable: {}'.format(cmd))
            
        if update or cmd not in self.settings:
            self.sync_local_setting(cmd)
            
        return self.settings[cmd]

    def set(self, cmd, value):
        '''Set command value.
        
        Args:
            cmd (str): Command to set value for
            value (int): Command value to set

        Returns:
            int: Command value

        Raises:
            ValueError: Invalid QDX command
            ValueError: Command is not settable (not in QDX.SET_COMMANDS)
        '''
        if cmd not in QDX.COMMANDS:
            raise ValueError('Invalid QDX command: {}'.format(cmd))
            
        if cmd not in QDX.SET_COMMANDS:
            raise ValueError('Command is not settable: {}'.format(cmd))
            
        self._set(cmd, value)
        return self.get(cmd, update=True)

    def sync_local_setting(self, cmd):
        '''Sync local setting with transceiver setting.

        Args:
            cmd (str): Command to sync

        Raises:
            ValueError: Invalid QDX command
            ValueError: Error processing command
        '''
        with self._settings_lock:
            if cmd not in QDX.COMMANDS:
                raise ValueError('Invalid QDX command: {}'.format(cmd))

            self.settings[cmd] = self._get(cmd)
    
    def sync_local_settings(self):
        '''Sync all local settings with transceiver settings.'''
        for cmd in QDX.COMMANDS:
            self.sync_local_setting(cmd)

    def ptt_on(self):
        '''Set PTT to transmit state.'''
        self.set(QDX.TX_STATE, 1)
                          
    def ptt_off(self):
        '''Set PTT to receive state.'''
        self.set(QDX.TX_STATE, 0)
        
    def toggle_ptt(self):
        '''Toggle PTT state.'''
        if self.get(QDX.TX_STATE) == 0:
            self.ptt_on()
        else:
            self.ptt_off()
    
    def _serial_request(self, request, device=None):
        '''Process serial request and response.

        Args:
            request (str): Command to get, or command and value to set
            device (str): Serial device port *str* to use instead of configured port, defaults to None

        Raises:
            ValueError: Serial port not specified
            OSError: Error during serial port request/response
        '''
        if device is None:
            device = self._port
        
        if device is None:
            raise ValueError('Serial port not specified')

        if self._debug:
            print( 'TX: {}'.format(request) )

        # convert string to bytes
        request = request.encode('utf-8')
                
        try:
            with serial.Serial(device, self._baudrate, timeout=self._timeout) as serial_port:
                serial_port.write(request)
                #TODO use while loop to wait until in_waiting is True, accounting for timeout
                time.sleep(0.1)
        
                response = b''
                if serial_port.in_waiting:
                    # handle pyserial library change in version 3.5
                    if float(serial.__version__) >= 3.5:
                        response = serial_port.read_until(expected=b';')
                    else:
                        response = serial_port.read_until(terminator=b';')
                        
        except Exception as e:
            raise OSError('Error during serial port request/response {}, check device connection'.format(device))
        
        # decode bytes to string
        response = response.decode('utf-8')
        # remove empty byte at the end of some returned values
        response = response.replace('\x00', '')

        if self._debug:
            print( 'RX: {}\n'.format(response) )
        
        # command was not understood
        if response == '?;':
            return None
            
        # remove leading command and trailing semicolon
        response = response[2:-1]
        return response

    def _get(self, cmd):
        '''Low level *get* operation handling.

        Args:
            cmd (str): Command to get value for

        Returns:
            int: Command value

        Other value types may be returned in the case of custom command handling (ex. dict)
        '''
        if cmd not in QDX.GET_COMMANDS:
            return None

        # handle custom command variants with leading underscore
        # same command, different response handling (ex. parse to dict)
        original_cmd = cmd
        cmd = cmd.replace('_', '')
        
        request = '{};'.format(cmd)
        response = self._serial_request(request)

        if value is None:
            return None

        # type conversion
        if response == '':
            return None
        elif response.replace('-', '', 1).isnumeric():
            # handle negative sign in string
             value = int(response)
        elif '.' in response and response.replace('.', '', 1).replace('-', '', 1).isnumeric():
            # handle decimal point and negative sign in string
            value = float(response)

        if original_cmd == QDX.RADIO_INFO_DICT:
            value = value.split('     ')

            value = {
                'vfo_freq': int(value[0]),
                'rit_offset': int(value[1][0:4]),
                'rit': bool(int(value[1][5])),
                'xit': bool(int(value[1][6])),
                'memory_bank': int(value[1][7]),
                'memory_channel': int(value[1][8:9]),
                'tx': bool(int(value[1][10])),
                'rx': not(bool(int(value[1][10]))),
                'mode': list(['USB', 'LSB', 'USB', 'USB'])[int(value[1][11])], # use value as list index
                'rx_vfo': list(['A', 'B'])[int(value[1][12])], # use value as list index
                'scan': bool(int(value[1][13])),
                'split': bool(int(value[1][14])),
                'tone': int(value[1][15]),
                'tone_number': int(value[1][16])
            }

        elif original_cmd == QDX.VERSION:
            value = float( value.replace('_', '.') )
        
        return value

    def _set(self, cmd, value):
        '''Low level *set* operation handling.

        Args:
            cmd (str): Command to get value for
            value (int): Command value to set
        '''
        if cmd not in QDX.SET_COMMANDS:
            return None
        
        # handle custom command variants with leading underscore
        # same command, different response handling (ex. parse to dict)
        original_cmd = cmd
        cmd = cmd.replace('_', '')
        
        request = '{}{};'.format(cmd, int(value))
        self._serial_request(request)
