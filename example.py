import qdx

try:
    radio = qdx.QDX()
    if radio.port:
        print('QDX found at ' + radio.port)
except Exception as e:
    print(e)
    exit()

vfo_a_freq = radio.get_vfo_a()
print('VFO A: ' + str(vfo_a_freq / 1000000) + ' MHz')

new_freq = float(input('\nEnter new frequency in MHz: ')) * 100000
radio.set_vfo_a(new_freq)
new_vfo_a_freq = radio.get_vfo_a()
print('VFO A: ' + str(new_vfo_a_freq / 1000000) + ' MHz')

input('\nPress enter to reset VFO A...')
radio.set_vfo_a(vfo_a_freq)
vfo_a_freq = radio.get_vfo_a()
print('VFO A: ' + str(vfo_a_freq / 1000000) + ' MHz')

