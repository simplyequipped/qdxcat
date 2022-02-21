import qdx

radio = qdx.QDX()

if radio.port:
    print('QDX found at' + radio.port)
else:
    print('QDX not found')
    exit()

commands = {}
for key, value in radio.__dict__.items():
    key = str(key)
    value = str(value)

    if key == 'baudrate' or key == 'port' or key == 'timeout':
        continue
    
    cmd = value['cmd']
    getter = value['get']
    setter = value['set']

# test
# 1. get current value and store
# 2. increment current value and store
# 3. set incremented value
# 4. get current value and compare to incremented value
# 5. pass / fail
# 6. set original value

