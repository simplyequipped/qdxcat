import qdx

try:
    radio = qdx.QDX()
    if radio.port:
        print('QDX found at ' + radio.port)
except Exception as e:
    print(e)
    exit()



# Option A: using individual command functions directly

# get vfo a freq
vfo_a_freq = radio.get_vfo_a()
print('VFO A: ' + str(vfo_a_freq / 1000000) + ' MHz')

# get new freq from user
new_freq = float(input('\nEnter new frequency in MHz: ')) * 100000
# set vfo a freq
radio.set_vfo_a(new_freq)
# get vfo a freq to confirm change
new_vfo_a_freq = radio.get_vfo_a()
print('VFO A: ' + str(new_vfo_a_freq / 1000000) + ' MHz')

# reset vfo a freq to original value
input('\nPress enter to reset VFO A...')
radio.set_vfo_a(vfo_a_freq)
vfo_a_freq = radio.get_vfo_a()
print('VFO A: ' + str(vfo_a_freq / 1000000) + ' MHz')



# Option B: using command utility function and tracked settings

# get vfo a freq (no read required, settings are read from the QDX when object is initiallized)
vfo_a_freq = radio.settings['FA']['value']
print('VFO A: ' + str(vfo_a_freq / 1000000) + ' MHz')

# get new freq from user
new_freq = float(input('\nEnter new frequency in MHz: ')) * 100000
# set vfo a freq (new setting is read from QDX automatically to confirm change)
radio.command('FA', new_freq)
# get vfo a freq
vfo_a_freq = radio.settings['FA']['value']
print('VFO A: ' + str(new_vfo_a_freq / 1000000) + ' MHz')

# reset vfo a freq to original value
input('\nPress enter to reset VFO A...')
radio.command('FA', vfo_a_freq)
vfo_a_freq = radio.settings['FA']['value']
print('VFO A: ' + str(vfo_a_freq / 1000000) + ' MHz')
