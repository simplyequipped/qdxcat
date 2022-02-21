import sys
import qdx

radio = qdx.QDX()

if radio.port:
    print('QDX found at' + radio.port)
else:
    print('QDX not found')
    exit()

tx = False
for arg in sys.argv:
    if arg.lower() in ['--tx', '-t']:
        tx = True

total = 0
passed = 0
failed = 0
skipped = 0

failed_cmds = {}
skipped_cmds = {}

for cmd in radio.commands:
    print('\n' + cmd['label'] + ' (' + cmd['cmd'] + ')')

    # skip tx command unless specified by user
    if cmd['cmd'] == 'TX' and tx == False:
        print('   skipping TX command')
        total += 1
        skipped += 1
        skipped_cmds[cmd['cmd']] = cmd['label']
        continue

    # get test
    try:
        total += 1
        if cmd['get'] is not None:
            value = radio.command(cmd['cmd'])
            if value is None:
                raise Exception('Command not understood')
    except Exception as e:
        failed += 1
        failed_cmds['get ' + cmd['label']] = cmd['cmd']
        print('   get: fail')
        print('      ' + str(e))
    else:
        if cmd['get'] is None:
            passed += 1
            print('   get: None')
        else:
            passed += 1
            print('   get: pass')

            if cmd['map'] is None:
                print('      ' + str(value))
            else:
                for key, val in cmd['map'].items():
                    if key == str(value):
                        print('      ' + str(val) + ' (' + str(value) + ')')
                        break

    # set test
    try:
        total += 1
        if cmd['set'] is not None:
            if value is None:
                if cmd['map'] is not None:
                    if '0' in cmd['map'].keys():
                        value = 0
                    else:
                        for key, val in cmd['map'].items():
                            value = key
                            break
                else:
                    raise Exception('no known value to set')
            else:
                radio.command(cmd['cmd'], value)
    except Exception as e:
        failed += 1
        failed_cmds['set ' + cmd['label']] = cmd['cmd']
        print('   set: fail')
        print('      ' + str(e))
    else:
        if cmd['set'] is None:
            passed += 1
            print('   set: None')
        else:
            passed += 1
            print('   set: pass')


print('\n\nTest Summary:')
print('   ' + str(passed) + '/' + str(total) + ' passed')
print('   ' + str(skipped) + '/' + str(total) + ' skipped')
for label, cmd in skipped_cmds.items():
    print('      ' + label + ' (' + cmd + ')')
print('   ' + str(failed) + '/' + str(total) + ' failed')
for label, cmd in failed_cmds.items():
    print('      ' + label + ' (' + cmd + ')')
print('')


