#import re, subprocess, time
import os, sys, time
import serial

class QDX:


    def __init__(self, port = None, discover = True):
        # QDX CAT commands
        # Kenwood TS-480/TS-440 command set
        self.AF_GAIN         = {'cmd': 'AG', 'get': self.get_af_gain,               'set': self.set_af_gain,                'label': 'Audio Gain',          'unit': '',     'map': None} 
        self.SIG_GEN_FREQ    = {'cmd': 'C2', 'get': self.get_sig_gen_freq,          'set': self.set_sig_gen_freq,           'label': 'Signal Gen',          'unit': 'Hz',   'map': None} 
        self.VFO_A           = {'cmd': 'FA', 'get': self.get_vfo_a,                 'set': self.set_vfo_a,                  'label': 'VFO A',               'unit': 'Hz',   'map': None} 
        self.VFO_B           = {'cmd': 'FB', 'get': self.get_vfo_b,                 'set': self.set_vfo_b,                  'label': 'VFO B',               'unit': 'Hz',   'map': None} 
        self.RX_VFO_MODE     = {'cmd': 'FR', 'get': self.get_rx_vfo_mode,           'set': self.set_rx_vfo_mode,            'label': 'RX VFO Mode',         'unit': '',     'map': {'0':'VFO A', '1':'VFO B', '2':'Split'}} 
        self.TX_VFO_MODE     = {'cmd': 'FT', 'get': self.get_tx_vfo_mode,           'set': self.set_tx_vfo_mode,            'label': 'TX VFO Mode',         'unit': '',     'map': {'0':'VFO A', '1':'VFO B', '2':'Split'}} 
        self.FILTER_BW       = {'cmd': 'FW', 'get': self.get_filter_bw,             'set': None,                            'label': 'Filter Bandwidth',    'unit': 'Hz',   'map': None} 
        self.RADIO_ID        = {'cmd': 'ID', 'get': self.get_radio_id,              'set': None,                            'label': 'Radio ID',            'unit': '',     'map': None} 
        self.RADIO_INFO      = {'cmd': 'IF', 'get': self.get_radio_info_dict,       'set': None,                            'label': 'Radio Info',          'unit': '',     'map': None} 
        self.OPERATING_MODE  = {'cmd': 'MD', 'get': self.get_operating_mode,        'set': self.set_operating_mode,         'label': 'Operating Mode',      'unit': '',     'map': {'1':'LSB', '3':'USB'}} 
        self.TXCO_FREQ       = {'cmd': 'Q0', 'get': self.get_txco_freq,             'set': self.set_txco_freq,              'label': 'TXCO',                'unit': 'Hz',   'map': None} 
        self.SIDEBAND        = {'cmd': 'Q1', 'get': self.get_sideband,              'set': self.set_sideband,               'label': 'Sideband',            'unit': '',     'map': {'0':'USB', '1':'LSB'}} 
        self.DEFAULT_FREQ    = {'cmd': 'Q2', 'get': self.get_default_freq,          'set': self.set_default_freq,           'label': 'Default Freq',        'unit': 'Hz',   'map': None} 
        self.RX_GAIN         = {'cmd': 'Q3', 'get': self.get_rx_gain,               'set': self.set_rx_gain,                'label': 'RX Gain',             'unit': '',     'map': None} 
        self.VOX_EN          = {'cmd': 'Q4', 'get': self.get_vox_enable,            'set': self.set_vox_enable,             'label': 'VOX',                 'unit': '',     'map': {'0':'Off', '1':'On'}} 
        self.TX_RISE         = {'cmd': 'Q5', 'get': self.get_tx_rise_threshold,     'set': self.set_tx_rise_threshold,      'label': 'TX Rise',             'unit': '',     'map': None} 
        self.TX_FALL         = {'cmd': 'Q6', 'get': self.get_tx_fall_threshold,     'set': self.set_tx_fall_threshold,      'label': 'TX Fall',             'unit': '',     'map': None} 
        self.CYCLE_MIN       = {'cmd': 'Q7', 'get': self.get_cycle_min_parameter,   'set': self.set_cycle_min_parameter,    'label': 'Cycle Min',           'unit': '',     'map': None} 
        self.SAMPLE_MIN      = {'cmd': 'Q8', 'get': self.get_sample_min_parameter,  'set': self.set_sample_min_parameter,   'label': 'Sample Min',          'unit': '',     'map': None} 
        self.DISCARD         = {'cmd': 'Q9', 'get': self.get_discard_parameter,     'set': self.set_discard_parameter,      'label': 'Discard',             'unit': '',     'map': None} 
        self.IQ_MODE         = {'cmd': 'QA', 'get': self.get_iq_mode,               'set': self.set_iq_mode,                'label': 'IQ Mode',             'unit': '',     'map': {'0':'Off', '1':'On'}} 
        self.JAPAN_BAND_LIM  = {'cmd': 'QB', 'get': self.get_japan_band_limit_mode, 'set': self.set_japan_band_limit_mode,  'label': 'Japan Band Mode',     'unit': '',     'map': {'0':'Off', '1':'On'}} 
        self.NEG_RIT_OFFSET  = {'cmd': 'RD', 'get': None,                           'set': self.set_negative_rit_offset,    'label': 'Neg RIT Offset',      'unit': '',     'map': None} 
        self.RIT_STATUS      = {'cmd': 'RT', 'get': self.get_rit_status,            'set': None,                            'label': 'RIT',                 'unit': '',     'map': {'0':'Off', '1':'On'}} 
        self.POS_RIT_OFFSET  = {'cmd': 'RU', 'get': None,                           'set': self.set_positive_rit_offset,    'label': 'Pos RIT Offset',      'unit': '',     'map': None} 
        self.RX_MODE         = {'cmd': 'RX', 'get': None,                           'set': self.set_rx,                     'label': 'RX',                  'unit': '',     'map': None} 
        self.SPLIT_MODE      = {'cmd': 'SP', 'get': self.get_split_mode,            'set': self.set_split_mode,             'label': 'Split Mode',          'unit': '',     'map': {'0':'Off', '1':'On'}} 
        self.TX_STATE        = {'cmd': 'TQ', 'get': self.get_tx_state,              'set': self.set_tx_state,               'label': 'RX/TX State',         'unit': '',     'map': {'0':'RX', '1':'TX'}} 
        self.TX_MODE         = {'cmd': 'TX', 'get': None,                           'set': self.set_tx,                     'label': 'TX',                  'unit': '',     'map': None} 

        self.commands = [self.VFO_A, self.VFO_B, self.RX_VFO_MODE, self.TX_VFO_MODE,self.FILTER_BW, self.RADIO_ID, self.RADIO_INFO, self.OPERATING_MODE, self.TXCO_FREQ, self.SIDEBAND,
                self.DEFAULT_FREQ, self.RX_GAIN, self.VOX_EN, self.TX_RISE, self.TX_FALL, self.CYCLE_MIN,self.SAMPLE_MIN, self.DISCARD, self.IQ_MODE, self.JAPAN_BAND_LIM,
                self.NEG_RIT_OFFSET,self.RIT_STATUS, self.POS_RIT_OFFSET, self.RX_MODE, self.SPLIT_MODE, self.TX_STATE, self.TX_MODE, self.AF_GAIN, self.SIG_GEN_FREQ]

        # serial port config
        self.port = port
        self.baudrate = 9600
        self.timeout = 1

        self.settings = {}

        if self.port == None and discover == True:
            self.discover()

    def discover(self):
        self.port = None
        if not os.path.isdir('/dev/serial/by-id'):
            raise Exception('QDX device not found, try specifying a serial port')
            return None

        qdx_devices = []
        with os.scandir('/dev/serial/by-id/') as devices:
            for device in devices:
                if 'QDX' in device.name and device.is_symlink():
                    symlink_path = os.readlink(device.path)
                    if '../' in symlink_path:
                        dev = os.path.abspath('/dev/serial/by-id/' + symlink_path)
                    else:
                        dev = symlink_path

                    qdx_devices.append(dev)

        if len(qdx_devices) == 1:
            self.set_port(qdx_devices[0])
        elif len(qdx_devices) > 1:
            raise Exception('Multiple QDX devices found, try specifying a serial port')
        else:
            raise Exception('QDX device not found, try specifiying a serial port')

        return None

    def set_port(self, port):
        if port != None:
            self.port = str(port)
            self.update_settings()

    def command(self, cat_cmd, value = None):
        for cmd in self.commands:
            if cmd['cmd'] == cat_cmd:
                if value == None and cmd['get'] != None:
                    return cmd['get']()
                elif cmd['set'] != None:
                    cmd['set'](value)
                    if cmd['cmd'] in self.settings.keys() and cmd['get'] != None:
                        self.settings[cmd['cmd']]['value'] = cmd['get']()
                    return None

    def update_settings(self):
        # TODO these commands do not appear to work correctly at the moment, 02/19/2022
        ignore_cmd = ['IF', 'ID', 'AG', 'Q0', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'QA', 'QB', 'RT']
        if self.port != None:
            for cmd in self.commands:
                if cmd['get'] != None and cmd['cmd'] not in ignore_cmd:
                    self.settings[cmd['cmd']] = {'value': cmd['get'](), 'label': cmd['label'], 'unit': cmd['unit'], 'map': cmd['map']}

    def __serial_request(self, cmd, value = None):
        if value != None:
            request = str(cmd) + str(value) + ';'
        else:
            request = str(cmd) + ';'
        request = request.encode('utf-8')

        try:
            with serial.Serial(self.port, self.baudrate, timeout=self.timeout) as serial_port:
                serial_port.write(request)
                time.sleep(0.1)
        
                response = b''
                if serial_port.in_waiting:
                    # handle pyserial library change in version 3.5
                    if float(serial.__version__) >= 3.5:
                        response = serial_port.read_until(expected=b';')
                    else:
                        response = serial_port.read_until(terminator=b';')
        except Exception as e:
            raise Exception('Error with serial port ' + self.port + ', check device connection')
        
        response = response.decode('utf-8')
        if response == '?;':
            return None
        # remove leading command str and trailing semicolon
        response = response[2:-1]
        return response
    
    # TODO check if some command reaponses should be float instead of int, error could be :
    # 'invalid literal for int() with base 10'

    # TODO CAT command not working
    def get_af_gain(self):
        gain = self.__serial_request(self.AF_GAIN['cmd'])
        if gain != None:
            gain = int(gain)
        return gain

    # TODO CAT command not working
    def set_af_gain(self, value):
        value = int(value)
        self.__serial_request(self.AF_GAIN['cmd'], value)

    def get_sig_gen_freq(self):
        freq = self.__serial_request(self.SIG_GEN_FREQ['cmd'])
        if freq != None:
            freq = int(freq)
        return freq

    def set_sig_gen_freq(self, value):
        value = int(value)
        self.__serial_request(self.SIG_GEN_FREQ['cmd'], value)

    def get_vfo_a(self):
        freq = self.__serial_request(self.VFO_A['cmd'])
        if freq != None:
            freq = int(freq)
        return freq

    def set_vfo_a(self, value):
        value = int(value)
        self.__serial_request(self.VFO_A['cmd'], value)

    def get_vfo_b(self):
        freq = self.__serial_request(self.VFO_B['cmd'])
        if freq != None:
            freq = int(freq)
        return freq

    def set_vfo_b(self, value):
        value = int(value)
        self.__serial_request(self.VFO_B['cmd'], value)

    def get_rx_vfo_mode(self):
        mode = self.__serial_request(self.RX_VFO_MODE['cmd'])
        if mode != None:
            mode = int(mode)
        return mode

    def set_rx_vfo_mode(self, value):
        value = int(value)
        self.__serial_request(self.RX_VFO_MODE['cmd'], value)
    
    def get_tx_vfo_mode(self):
        mode = self.__serial_request(self.TX_VFO_MODE['cmd'])
        if mode != None:
            mode = int(mode)
        return mode

    def set_tx_vfo_mode(self, value):
        value = int(value)
        self.__serial_request(self.TX_VFO_MODE['cmd'], value)
        
    def get_filter_bw(self):
        bw = self.__serial_request(self.FILTER_BW['cmd'])
        if bw != None:
            bw = int(bw)
        return bw

    def get_radio_id(self):
        radio_id = self.__serial_request(self.RADIO_ID)
        if radio_id != None:
            radio_id = int(radio_id)
        return radio_id

    def get_radio_info(self):
        info = self.__serial_request(self.RADIO_INFO['cmd'])
        return info

    def get_radio_info_dict(self):
        info_dict = {}
        info = self.__serial_request(self.RADIO_INFO['cmd'])

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
        mode = self.__serial_request(self.OPERATING_MODE['cmd'])
        if mode != None:
            mode = int(mode)
        return mode

    def set_operating_mode(self, value):
        value = int(value)
        self.__serial_request(self.OPERATING_MODE['cmd'], value)

    # TODO CAT command not working
    def get_txco_freq(self):
        freq = self.__serial_request(self.TXCO_FREQ['cmd'])
        if freq != None:
            freq = int(freq)
        return freq

    # TODO CAT command not working
    def set_txco_freq(self, value):
        value = int(value)
        self.__serial_request(self.TXCO_FREQ['cmd'], value)

    # TODO CAT command not working
    def get_sideband(self):
        sideband = self.__serial_request(self.SIDEBAND['cmd'])
        if sideband != None:
            sideband = int(sideband)
        return sideband

    # TODO CAT command not working
    def set_sideband(self, value):
        value = int(value)
        self.__serial_request(self.SIDEBAND['cmd'], value)

    # TODO CAT command not working
    def get_default_freq(self):
        freq = self.__serial_request(self.DEFAULT_FREQ['cmd'])
        if freq != None:
            freq = int(freq)
        return freq

    # TODO CAT command not working
    def set_default_freq(self, value):
        value = int(value)
        self.__serial_request(self.DEFAULT_FREQ['cmd'], value)

    # TODO CAT command not working
    def get_rx_gain(self):
        gain = self.__serial_request(self.RX_GAIN['cmd'])
        if gain != None:
            gain = int(gain)
        return gain

    # TODO CAT command not working
    def set_rx_gain(self, value):
        value = int(value)
        self.__serial_request(self.RX_GAIN['cmd'], value)

    # TODO CAT command not working
    def get_vox_enable(self):
        vox = self.__serial_request(self.VOX_EN['cmd'])
        if vox != None:
            vox = int(vox)
        return vox

    # TODO CAT command not working
    def set_vox_enable(self, value):
        value = int(value)
        self.__serial_request(self.VOX_EN['cmd'], value)

    # TODO CAT command not working
    def get_tx_rise_threshold(self):
        threshold = self.__serial_request(self.TX_RISE['cmd'])
        if threshold != None:
            threshold = int(threshold)
        return threshold

    # TODO CAT command not working
    def set_tx_rise_threshold(self, value):
        value = int(value)
        self.__serial_request(self.TX_RISE['cmd'], value)

    # TODO CAT command not working
    def get_tx_fall_threshold(self):
        threshold = self.__serial_request(self.TX_FALL['cmd'])
        if threshold != None:
            threshold = int(threshold)
        return threshold

    # TODO CAT command not working
    def set_tx_fall_threshold(self, value):
        value = int(value)
        self.__serial_request(self.TX_FALL['cmd'], value)

    # TODO CAT command not working
    def get_cycle_min_parameter(self):
        parameter = self.__serial_request(self.CYCLE_MIN['cmd'])
        if parameter != None:
            parameter = int(parameter)
        return parameter

    # TODO CAT command not working
    def set_cycle_min_parameter(self, value):
        value = int(value)
        self.__serial_request(self.CYCLE_MIN['cmd'], value)

    # TODO CAT command not working
    def get_sample_min_parameter(self):
        parameter = self.__serial_request(self.SAMPLE_MIN['cmd'])
        if parameter != None:
            parameter = int(parameter)
        return parameter

    # TODO CAT command not working
    def set_sample_min_parameter(self, value):
        value = int(value)
        self.__serial_request(self.SAMPLE_MIN['cmd'], value)

    # TODO CAT command not working
    def get_discard_parameter(self):
        parameter = self.__serial_request(self.DISCARD['cmd'])
        if parameter != None:
            parameter = int(parameter)
        return parameter

    # TODO CAT command not working
    def set_discard_parameter(self, value):
        value = int(value)
        self.__serial_request(self.DISCARD['cmd'], value)

    # TODO CAT command not working
    def get_iq_mode(self):
        mode = self.__serial_request(self.IQ_MODE['cmd'])
        if mode != None:
            mode = int(mode)
        return mode

    # TODO CAT command not working
    def set_iq_mode(self, value):
        value = int(value)
        self.__serial_request(self.IQ_MODE['cmd'], value)

    # TODO CAT command not working
    def get_japan_band_limit_mode(self):
        mode = self.__serial_request(self.JAPAN_BAND_LIM['cmd'])
        if mode != None:
            mode = int(mode)
        return mode

    # TODO CAT command not working
    def set_japan_band_limit_mode(self, value):
        value = int(value)
        self.__serial_request(self.JAPAN_BAND_LIM['cmd'], value)

    # TODO no RIT get method supported per QDX docs
    def set_negative_rit_offset(self, value):
        value = int(value)
        self.__serial_request(self.NEG_RIT_OFFSET['cmd'], value)

    def get_rit_status(self):
        status = self.__serial_request(self.RIT_STATUS['cmd'])
        if status != None:
            status = int(status)
        return status
    
    # TODO no RIT get method supported per QDX docs
    def set_positive_rit_offset(self, value):
        value = int(value)
        self.__serial_request(self.POS_RIT_OFFSET['cmd'], value)

    def set_rx(self):
        self.__serial_request(self.RX_MODE['cmd'])

    def get_split_mode(self):
        mode = self.__serial_request(self.SPLIT_MODE['cmd'])
        if mode != None:
            mode = int(mode)
        return mode

    def set_split_mode(self, value):
        value = int(value)
        self.__serial_request(self.SPLIT_MODE['cmd'], value)

    def get_tx_state(self):
        state = self.__serial_request(self.TX_STATE['cmd'])
        if state != None:
            state = int(state)
        return state

    def set_tx_state(self, value):
        value = int(value)
        self.__serial_request(self.TX_STATE['cmd'], value)

    def set_tx(self):
        self.__serial_request(self.TX_MODE['cmd'])


