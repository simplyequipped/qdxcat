from flask import Flask, render_template, request, redirect
import qdx
import sys

app = Flask(__name__)
radio = qdx.QDX(discover = False)

@app.route('/')
def index():
    global radio
    serial_port = None

    if len(request.args):
        serial_port = request.args.get('port')

    try:
        if serial_port != None:
            radio.set_port(serial_port)
        else:
            radio.discover()

    except Exception as e:
        return render_template('radio_error.html', msg=e)
    else:
        return redirect('/settings')

@app.route('/settings')
def settings():
    global radio
    return render_template('settings.html', settings=radio.settings, port=radio.port)

@app.route('/set', methods=['POST'])
def set_value():
    global radio
    # get the posted command and new value
    for cmd, value in request.form.items():
        try:
            #issue the command to the radio
            radio.command(cmd, value)

        except Exception as e:
            pass
        
        # return the updated value to the page
        return str(radio.settings[cmd]['value'])

@app.route('/heartbeat')
def heartbeat():
    global radio
    try:
        #get radio state
        tx = radio.command('TQ')
        if tx:
            return 'TX'
        else:
            return 'RX'

    except Exception as e:
        return 'Error'




def dev_server():
    app.run(host='0.0.0.0')
