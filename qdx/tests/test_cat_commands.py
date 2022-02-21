import qdx

radio = qdx.QDX()

if radio.port:
    print('QDX found at' + radio.port)
else:
    print('QDX not found')
    exit()

for cmd in radio.commands:
    print('\n' + cmd['label'] + ' (' + cmd['cmd'] + ')')

    # get test
    try:
        if cmd['get'] is not None:
            value = radio.command(cmd['cmd'])
    except Exception as e:
        print('\tget: fail')
        print('\t\t' + e)
    else:
        if cmd['get'] is None:
            print('get: None')
        else:
            print('\tget: pass')

            if cmd['map'] is None:
                print('\t\t' + str(value))
            else:
                for key, val in cmd['map']:
                    if key == str(value):
                        print('\t\t' + val + ' (' + value + ')')
                        break

    # set test
    try:
        if cmd['set'] is not None:
            if value is None:
                if cmd['map'] is not None:
                    if '0' in cmd['map'].keys():
                        value = 0
                    else:
                        for key, val in cmd['map']:
                            value = key
                            break
                else:
                    raise Exception('no known value to set')
            else:
                radio.command(cmd['cmd'], value)
    except Exception as e:
        print('\tset: fail')
        print('\t\t' + e)
    else:
        if cmd['set'] is None:
            print('set: None')
        else:
            print('\set: pass')

