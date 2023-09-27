import time
import serial
import threading

from serial.tools.list_ports import grep


#TODO
# update map options to map int values to str option labels

class QDX:
    # QDX CAT commands
    # Kenwood TS-480/TS-440 command set
    AF_GAIN         = 'AG'
    SIG_GEN_FREQ    = 'C2'
    VFO_A           = 'FA'
    VFO_B           = 'FB'
    RX_VFO_MODE     = 'FR'
    TX_VFO_MODE     = 'FT'
    FILTER_BW       = 'FW'
    RADIO_ID        = 'ID'
    RADIO_INFO      = 'IF'
    OPERATING_MODE  = 'MD'
    TXCO_FREQ       = 'Q0'
    SIDEBAND        = 'Q1'
    DEFAULT_FREQ    = 'Q2'
    RX_GAIN         = 'Q3'
    VOX_EN          = 'Q4'
    TX_RISE         = 'Q5'
    TX_FALL         = 'Q6'
    CYCLE_MIN       = 'Q7'
    SAMPLE_MIN      = 'Q8' 
    DISCARD         = 'Q9'
    IQ_MODE         = 'QA'
    JAPAN_BAND_LIM  = 'QB'
    NEG_RIT_OFFSET  = 'RD'
    RIT_STATUS      = 'RT' 
    POS_RIT_OFFSET  = 'RU'
    RX_MODE         = 'RX'
    SPLIT_MODE      = 'SP'
    TX_STATE        = 'TQ'
    TX_MODE         = 'TX'

    # added in firmware v1.05
    VERSION         = 'VN'

    # added in firmware v1.06
    CAT_TIMEOUT     = 'QC'
    PTT_PORT_SERIAL = 'QD'
    VGA_PS2_MODE    = 'QE'
    SERIAL1_BAUD    = 'QF'
    SERIAL2_BAUD    = 'QG'
    SERIAL3_BAUD    = 'QH'
    NIGHT_MODE      = 'QI'
    TX_SHIFT        = 'QJ'
    

    COMMANDS = [AF_GAIN, SIG_GEN_FREQ, VFO_A, VFO_B, RX_VFO_MODE, TX_VFO_MODE, FILTER_BW, RADIO_ID, RADIO_INFO, OPERATING_MODE, TXCO_FREQ, SIDEBAND, DEFAULT_FREQ, RX_GAIN, VOX_EN,
        TX_RISE, TX_FALL, CYCLE_MIN, SAMPLE_MIN, DISCARD, IQ_MODE, JAPAN_BAND_LIM, NEG_RIT_OFFSET, RIT_STATUS, POS_RIT_OFFSET, RX_MODE, SPLIT_MODE, TX_STATE, TX_MODE, VERSION,
        CAT_TIMEOUT, PTT_PORT_SERIAL, VGA_PS2_MODE, SERIAL1_BAUD, SERIAL2_BAUD, SERIAL3_BAUD, NIGHT_MODE, TX_SHIFT]
    
    def __init__(self, port=None, autodetect=True):        
        self.command_map = {
            'AG' : {'get': self.get_af_gain,               'set': self.set_af_gain,                'label': 'Audio Gain',          'unit': '',     'options': None}, 
            'C2' : {'get': self.get_sig_gen_freq,          'set': self.set_sig_gen_freq,           'label': 'Signal Gen',          'unit': 'Hz',   'options': None}, 
            'FA' : {'get': self.get_vfo_a,                 'set': self.set_vfo_a,                  'label': 'VFO A',               'unit': 'Hz',   'options': None}, 
            'FB' : {'get': self.get_vfo_b,                 'set': self.set_vfo_b,                  'label': 'VFO B',               'unit': 'Hz',   'options': None}, 
            'FR' : {'get': self.get_rx_vfo_mode,           'set': self.set_rx_vfo_mode,            'label': 'RX VFO Mode',         'unit': '',     'options': {'0':'VFO A', '1':'VFO B', '2':'Split'}}, 
            'FT' : {'get': self.get_tx_vfo_mode,           'set': self.set_tx_vfo_mode,            'label': 'TX VFO Mode',         'unit': '',     'options': {'0':'VFO A', '1':'VFO B', '2':'Split'}}, 
            'FW' : {'get': self.get_filter_bw,             'set': None,                            'label': 'Filter Bandwidth',    'unit': 'Hz',   'options': None}, 
            'ID' : {'get': self.get_radio_id,              'set': None,                            'label': 'Radio ID',            'unit': '',     'options': None}, 
            'IF' : {'get': self.get_radio_info_dict,       'set': None,                            'label': 'Radio Info',          'unit': '',     'options': None}, 
            'MD' : {'get': self.get_operating_mode,        'set': self.set_operating_mode,         'label': 'Operating Mode',      'unit': '',     'options': {'1':'LSB', '3':'USB'}}, 
            'Q0' : {'get': self.get_txco_freq,             'set': self.set_txco_freq,              'label': 'TXCO',                'unit': 'Hz',   'options': None}, 
            'Q1' : {'get': self.get_sideband,              'set': self.set_sideband,               'label': 'Sideband',            'unit': '',     'options': {'0':'USB', '1':'LSB'}}, 
            'Q2' : {'get': self.get_default_freq,          'set': self.set_default_freq,           'label': 'Default Freq',        'unit': 'Hz',   'options': None}, 
            'Q3' : {'get': self.get_rx_gain,               'set': self.set_rx_gain,                'label': 'RX Gain',             'unit': '',     'options': None}, 
            'Q4' : {'get': self.get_vox_enable,            'set': self.set_vox_enable,             'label': 'VOX',                 'unit': '',     'options': {'0':'Off', '1':'On'}}, 
            'Q5' : {'get': self.get_tx_rise_threshold,     'set': self.set_tx_rise_threshold,      'label': 'TX Rise',             'unit': '',     'options': None}, 
            'Q6' : {'get': self.get_tx_fall_threshold,     'set': self.set_tx_fall_threshold,      'label': 'TX Fall',             'unit': '',     'options': None}, 
            'Q7' : {'get': self.get_cycle_min_parameter,   'set': self.set_cycle_min_parameter,    'label': 'Cycle Min',           'unit': '',     'options': None}, 
            'Q8' : {'get': self.get_sample_min_parameter,  'set': self.set_sample_min_parameter,   'label': 'Sample Min',          'unit': '',     'options': None}, 
            'Q9' : {'get': self.get_discard_parameter,     'set': self.set_discard_parameter,      'label': 'Discard',             'unit': '',     'options': None}, 
            'QA' : {'get': self.get_iq_mode,               'set': self.set_iq_mode,                'label': 'IQ Mode',             'unit': '',     'options': {'0':'Off', '1':'On'}}, 
            'QB' : {'get': self.get_japan_band_limit_mode, 'set': self.set_japan_band_limit_mode,  'label': 'Japan Band Mode',     'unit': '',     'options': {'0':'Off', '1':'On'}}, 
            'RD' : {'get': None,                           'set': self.set_negative_rit_offset,    'label': 'Neg RIT Offset',      'unit': '',     'options': None}, 
            'RT' : {'get': self.get_rit_status,            'set': None,                            'label': 'RIT',                 'unit': '',     'options': {'0':'Off', '1':'On'}}, 
            'RU' : {'get': None,                           'set': self.set_positive_rit_offset,    'label': 'Pos RIT Offset',      'unit': '',     'options': None}, 
            'RX' : {'get': None,                           'set': self.set_rx,                     'label': 'RX',                  'unit': '',     'options': None}, 
            'SP' : {'get': self.get_split_mode,            'set': self.set_split_mode,             'label': 'Split Mode',          'unit': '',     'options': {'0':'Off', '1':'On'}}, 
            'TQ' : {'get': self.get_tx_state,              'set': self.set_tx_state,               'label': 'RX/TX State',         'unit': '',     'options': {'0':'RX', '1':'TX'}}, 
            'TX' : {'get': None,                           'set': self.set_tx,                     'label': 'TX',                  'unit': '',     'options': None},
            # added in firmware v1.05
            'VN' : {'get': self.get_version,               'set': None,                            'label': 'Firmware Version',    'unit': '',     'options': None},
            # added in firmware v1.06
            'QC' : {'get': self.get_cat_timeout,           'set': self.set_cat_timeout,            'label': 'CAT Timeout',         'unit': '',     'options': None},
            'QD' : {'get': self.get_ptt_port_serial,       'set': self.set_ptt_port_serial,        'label': 'PTT Port as Serial',  'unit': '',     'options': {'0':'Off', '1':'On'}},
            'QE' : {'get': self.get_vga_ps2_mode,          'set': self.set_vga_ps2_mode,           'label': 'VGA PS/2 Mode',       'unit': '',     'options': {'0':'Off', '1':'On'}},
            'QF' : {'get': self.get_serial1_baud,          'set': self.set_serial1_baud,           'label': 'Serial 1 Baud Rate',  'unit': '',     'options': None},
            'QG' : {'get': self.get_serial2_baud,          'set': self.set_serial2_baud,           'label': 'Serial 2 Baud Rate',  'unit': '',     'options': None},
            'QH' : {'get': self.get_serial3_baud,          'set': self.set_serial3_baud,           'label': 'Serial 3 Baud Rate',  'unit': '',     'options': None},
            'QI' : {'get': self.get_night_mode,            'set': self.set_night_mode,             'label': 'Night Mode',          'unit': '',     'options': {'0':'Off', '1':'On'}},
            'QJ' : {'get': self.get_tx_shift,              'set': self.set_tx_shift,               'label': 'TX Shift',            'unit': '',     'options': None}
        }

        self.settings = {}
        self._settings_lock = threading.Lock()
        
        # serial port config
        self.port = None
        self.baudrate = 9600
        self.timeout = 1

        if port is not None:
            self.set_port(port)
        elif autodetect:
            self.autodetect()

    def autodetect(self):
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

    def set_port(self, port, sync=True):
        if port is None:
            return
            
        self.port = port

        if sync:
            thread = threading.Thread(target=self.sync_local_settings)
            thread.daemon = True
            thread.start()

    def get(self, cmd, update=False):
        if cmd not in QDX.COMMANDS:
            raise ValueError('Invalid QDX command: {}'.format(cmd))
            
        if update or cmd not in self.settings:
            self.sync_local_setting(cmd)
        
        return self.settings[cmd]

    def set(self, cmd, value):
        if cmd not in QDX.COMMANDS:
            raise ValueError('Invalid QDX command: {}'.format(cmd))
            
        if self.command_map[cmd]['set'] is not None:
            # set command value
            self.command_map[cmd]['set'](value)

        return self.get(cmd, update=True)

    def sync_local_setting(self, cmd):
        with self._settings_lock:
            if cmd not in QDX.COMMANDS:
                raise ValueError('Invalid QDX command: {}'.format(cmd))
            
            if self.command_map[cmd]['get'] is not None:
                try:
                    self.settings[cmd] = self.command_map[cmd]['get']()
                except Exception as e:
                    raise ValueError('Error processing command: {}'.format(cmd)) from e
    
    def sync_local_settings(self):
        for cmd in QDX.COMMANDS:
            self.sync_local_setting(cmd)

    def ptt_on(self):
        self.set(QDX.TX_STATE, 1)
                          
    def ptt_off(self):
        self.set(QDX.TX_STATE, 0)
        
    def toggle_ptt(self):
        if self.get(QDX.TX_STATE) == 0:
            self.ptt_on()
        else:
            self.ptt_off()
    
    def _serial_request(self, cmd, value = None, device=None):
        if device is None:
            device = self.port
        
        if device is None:
            raise ValueError('Serial port not specified')
            
        # build command string
        if value is not None:
            # 'set' command
            request = str(cmd) + str(value) + ';'
        else:
            # 'get' command
            request = str(cmd) + ';'
            
        request = request.encode('utf-8')
                
        try:
            with serial.Serial(device, self.baudrate, timeout=self.timeout) as serial_port:
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
            raise OSError('Error on serial port {}, check device connection'.format(device))
        
        # decode bytes to response string
        response = response.decode('utf-8')
        # remove empty byte at the end of some returned values
        response = response.replace('\x00', '')
        
        # stop processing if the device did not understand the command
        if response == '?;':
            return None
            
        # remove leading command string and trailing semicolon
        response = response[2:-1]

        return response
    
    def get_af_gain(self):
        gain = self._serial_request(QDX.AF_GAIN)
        if gain is not None:
            gain = int(gain)
        return gain

    def set_af_gain(self, value):
        value = int(value)
        self._serial_request(QDX.AF_GAIN, value)

    def get_sig_gen_freq(self):
        freq = self._serial_request(QDX.SIG_GEN_FREQ)
        if freq is not None:
            freq = int(freq)
        return freq

    def set_sig_gen_freq(self, value):
        value = int(value)
        self._serial_request(QDX.SIG_GEN_FREQ, value)

    def get_vfo_a(self):
        freq = self._serial_request(QDX.VFO_A)
        if freq is not None:
            freq = int(freq)
        return freq

    def set_vfo_a(self, value):
        value = int(value)
        self._serial_request(QDX.VFO_A, value)

    def get_vfo_b(self):
        freq = self._serial_request(QDX.VFO_B)
        if freq is not None:
            freq = int(freq)
        return freq

    def set_vfo_b(self, value):
        value = int(value)
        self._serial_request(QDX.VFO_B, value)

    def get_rx_vfo_mode(self):
        mode = self._serial_request(QDX.RX_VFO_MODE)
        if mode is not None:
            mode = int(mode)
        return mode

    def set_rx_vfo_mode(self, value):
        value = int(value)
        self._serial_request(QDX.RX_VFO_MODE, value)
    
    def get_tx_vfo_mode(self):
        mode = self._serial_request(QDX.TX_VFO_MODE)
        if mode is not None:
            mode = int(mode)
        return mode

    def set_tx_vfo_mode(self, value):
        value = int(value)
        self._serial_request(QDX.TX_VFO_MODE, value)
        
    def get_filter_bw(self):
        bw = self._serial_request(QDX.FILTER_BW)
        if bw is not None:
            bw = int(bw)
        return bw

    def get_radio_id(self):
        radio_id = self._serial_request(QDX.RADIO_ID)
        if radio_id is not None:
            radio_id = int(radio_id)
        return radio_id

    def get_radio_info(self):
        info = self._serial_request(QDX.RADIO_INFO)
        return info

    def get_radio_info_dict(self):
        info_dict = {}
        info = self._serial_request(QDX.RADIO_INFO)

        if info == None:
            return None

        info = info.split('     ')

        info_dict['vfo_freq'] = int(info[0])
        info_dict['rit_offset'] = int(info[1][0:4])
        info_dict['rit'] = bool(int(info[1][5]))
        info_dict['xit'] = bool(int(info[1][6]))
        info_dict['memory_bank'] = int(info[1][7])
        info_dict['memory_channel'] = int(info[1][8:9])
        info_dict['tx'] = bool(int(info[1][10]))
        info_dict['rx'] = not(bool(int(info[1][10])))
        info_dict['mode'] = list(['USB', 'LSB', 'USB', 'USB'])[int(info[1][11])]
        info_dict['rx_vfo'] = list(['A', 'B'])[int(info[1][12])]
        info_dict['scan'] = bool(int(info[1][13]))
        info_dict['split'] = bool(int(info[1][14]))
        info_dict['tone'] = int(info[1][15])
        info_dict['tone_number'] = int(info[1][16])

        return info_dict

    def get_operating_mode(self):
        mode = self._serial_request(QDX.OPERATING_MODE)
        if mode is not None:
            mode = int(mode)
        return mode

    def set_operating_mode(self, value):
        value = int(value)
        self._serial_request(QDX.OPERATING_MODE, value)

    def get_txco_freq(self):
        freq = self._serial_request(QDX.TXCO_FREQ)
        if freq is not None:
            freq = int(freq)
        return freq

    def set_txco_freq(self, value):
        value = int(value)
        self._serial_request(QDX.TXCO_FREQ, value)

    def get_sideband(self):
        sideband = self._serial_request(QDX.SIDEBAND)
        if sideband is not None:
            sideband = int(sideband)
        return sideband

    def set_sideband(self, value):
        value = int(value)
        self._serial_request(QDX.SIDEBAND, value)

    def get_default_freq(self):
        freq = self._serial_request(QDX.DEFAULT_FREQ)
        if freq is not None:
            freq = int(freq)
        return freq

    def set_default_freq(self, value):
        value = int(value)
        self._serial_request(QDX.DEFAULT_FREQ, value)

    def get_rx_gain(self):
        gain = self._serial_request(QDX.RX_GAIN)
        if gain is not None:
            gain = int(gain)
        return gain

    def set_rx_gain(self, value):
        value = int(value)
        self._serial_request(QDX.RX_GAIN, value)

    def get_vox_enable(self):
        vox = self._serial_request(QDX.VOX_EN)
        if vox is not None:
            vox = int(vox)
        return vox

    def set_vox_enable(self, value):
        value = int(value)
        self._serial_request(QDX.VOX_EN, value)

    def get_tx_rise_threshold(self):
        threshold = self._serial_request(QDX.TX_RISE)
        if threshold is not None:
            threshold = int(threshold)
        return threshold

    def set_tx_rise_threshold(self, value):
        value = int(value)
        self._serial_request(QDX.TX_RISE, value)

    def get_tx_fall_threshold(self):
        threshold = self._serial_request(QDX.TX_FALL)
        if threshold is not None:
            threshold = int(threshold)
        return threshold

    def set_tx_fall_threshold(self, value):
        value = int(value)
        self._serial_request(QDX.TX_FALL, value)

    def get_cycle_min_parameter(self):
        parameter = self._serial_request(QDX.CYCLE_MIN)
        if parameter is not None:
            parameter = int(parameter)
        return parameter

    def set_cycle_min_parameter(self, value):
        value = int(value)
        self._serial_request(QDX.CYCLE_MIN, value)

    def get_sample_min_parameter(self):
        parameter = self._serial_request(QDX.SAMPLE_MIN)
        if parameter is not None:
            parameter = int(parameter)
        return parameter

    def set_sample_min_parameter(self, value):
        value = int(value)
        self._serial_request(QDX.SAMPLE_MIN, value)

    def get_discard_parameter(self):
        parameter = self._serial_request(QDX.DISCARD)
        if parameter is not None:
            parameter = int(parameter)
        return parameter

    def set_discard_parameter(self, value):
        value = int(value)
        self._serial_request(QDX.DISCARD, value)

    def get_iq_mode(self):
        mode = self._serial_request(QDX.IQ_MODE)
        if mode is not None:
            mode = int(mode)
        return mode

    def set_iq_mode(self, value):
        value = int(value)
        self._serial_request(QDX.IQ_MODE, value)

    def get_japan_band_limit_mode(self):
        mode = self._serial_request(QDX.JAPAN_BAND_LIM)
        if mode is not None:
            mode = int(mode)
        return mode

    def set_japan_band_limit_mode(self, value):
        value = int(value)
        self._serial_request(QDX.JAPAN_BAND_LIM, value)

    def set_negative_rit_offset(self, value):
        value = int(value)
        self._serial_request(QDX.NEG_RIT_OFFSET, value)

    def get_rit_status(self):
        status = self._serial_request(QDX.RIT_STATUS)
        if status is not None:
            status = int(status)
        return status
    
    def set_positive_rit_offset(self, value):
        value = int(value)
        self._serial_request(QDX.POS_RIT_OFFSET, value)

    def set_rx(self, value):
        self._serial_request(QDX.RX_MODE)

    def get_split_mode(self):
        mode = self._serial_request(QDX.SPLIT_MODE)
        if mode is not None:
            mode = int(mode)
        return mode

    def set_split_mode(self, value):
        value = int(value)
        self._serial_request(QDX.SPLIT_MODE, value)

    def get_tx_state(self):
        state = self._serial_request(QDX.TX_STATE)
        if state is not None:
            state = int(state)
        return state

    def set_tx_state(self, value):
        value = int(value)
        self._serial_request(QDX.TX_STATE, value)

    def set_tx(self, value):
        value = int(value)
        self._serial_request(QDX.TX_MODE)

    def get_version(self):
        state = self._serial_request(QDX.VERSION)
        if state is not None:
            state = float( state.replace('_', '.') )
        return state

    def get_cat_timeout(self):
        state = self._serial_request(QDX.CAT_TIMEOUT)
        if state is not None:
            state = int(state)
        return state

    def set_cat_timeout(self, value):
        value = int(value)
        self._serial_request(QDX.CAT_TIMEOUT, value)

    def get_ptt_port_serial(self):
        state = self._serial_request(QDX.PTT_PORT_SERIAL)
        if state is not None:
            state = int(state)
        return state

    def set_ptt_port_serial(self, value):
        value = int(value)
        self._serial_request(QDX.PTT_PORT_SERIAL, value)

    def get_vga_ps2_mode(self):
        state = self._serial_request(QDX.VGA_PS2_MODE)
        if state is not None:
            state = int(state)
        return state

    def set_vga_ps2_mode(self, value):
        value = int(value)
        self._serial_request(QDX.VGA_PS2_MODE, value)

    def get_serial1_baud(self):
        state = self._serial_request(QDX.SERIAL1_BAUD)
        if state is not None:
            state = int(state)
        return state

    def set_serial1_baud(self, value):
        value = int(value)
        self._serial_request(QDX.SERIAL1_BAUD, value)

    def get_serial2_baud(self):
        state = self._serial_request(QDX.SERIAL2_BAUD)
        if state is not None:
            state = int(state)
        return state

    def set_serial2_baud(self, value):
        value = int(value)
        self._serial_request(QDX.SERIAL2_BAUD, value)

    def get_serial3_baud(self):
        state = self._serial_request(QDX.SERIAL3_BAUD)
        if state is not None:
            state = int(state)
        return state

    def set_serial3_baud(self, value):
        value = int(value)
        self._serial_request(QDX.SERIAL3_BAUD, value)

    def get_night_mode(self):
        state = self._serial_request(QDX.NIGHT_MODE)
        if state is not None:
            state = int(state)
        return state

    def set_night_mode(self, value):
        value = int(value)
        self._serial_request(QDX.NIGHT_MODE, value)

    def get_tx_shift(self):
        state = self._serial_request(QDX.TX_SHIFT)
        if state is not None:
            state = int(state)
        return state

    def set_tx_shift(self, value):
        value = int(value)
        self._serial_request(QDX.TX_SHIFT, value)

