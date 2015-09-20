import os
from flask import Flask, Response, request
from twilio import twiml
from twilio.rest import TwilioRestClient
from flask import jsonify
from flask import render_template
from flask import url_for

#app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')
client = TwilioRestClient()
app.config.from_pyfile('local_settings.py')

# this should be your Twilio number, format: +14155551234
CUSTOMER_SERVICE_NUMBER = os.environ.get('CUSTOMER_SERVICE_NUMBER', '')
# your cell phone number (agent's number), format: +14155551234
AGENT1_NUMBER = os.environ.get('AGENT1_NUMBER', '')
# second person's phone or Twilio number if testing, format: +14155551234
AGENT2_NUMBER = os.environ.get('AGENT2_NUMBER', '')
# ngrok URL, such as "https://17224f9e.ngrok.io", no trailing slash
BASE_URL = os.environ.get('BASE_URL', 'https://143e6ab2.ngrok.io')


@app.route('/call', methods=['POST'])
def inbound_call():
    call_sid = request.form['CallSid']
    response = twiml.Response()
    response.dial().conference(call_sid)
    call = client.calls.create(to=AGENT1_NUMBER,
                               from_=CUSTOMER_SERVICE_NUMBER,
                               url=BASE_URL + '/conference/' + call_sid)
    return Response(str(response), 200, mimetype="application/xml")


@app.route('/conference/<conference_name>', methods=['GET', 'POST'])
def conference_line(conference_name):
    response = twiml.Response()
    response.dial(hangupOnStar=True).conference(conference_name)
    response.gather(action=BASE_URL + '/add-agent/' + conference_name,
                    numDigits=1)
    return Response(str(response), 200, mimetype="application/xml")


@app.route('/add-agent/<conference_name>', methods=['POST'])
def add_second_agent(conference_name):
    client.calls.create(to=AGENT2_NUMBER, from_=CUSTOMER_SERVICE_NUMBER,
                        url=BASE_URL + '/conference/' + conference_name)
    response = twiml.Response()
    response.dial(hangupOnStar=True).conference(conference_name)
    return Response(str(response), 200, mimetype="application/xml")


# this function is optional - for testing purposes if you don't have
# a third phone to call
@app.route('/agent-johnson-test', methods=['POST'])
def agent_johnson_test():
    response = twiml.Response()
    response.say("Hello, this is Agent Johnson.", loop=10)
    return Response(str(response), 200, mimetype="application/xml")

@app.route('/')
def index():
    return render_template('index.html',
                           configuration_error=None)


# Voice Request URL
@app.route('/click2call', methods=['POST'])
def call():
    # Get phone number we need to call
    phone_number = request.form.get('phoneNumber', None)

    try:
        twilio_client = TwilioRestClient(app.config['TWILIO_ACCOUNT_SID'],
                                         app.config['TWILIO_AUTH_TOKEN'])
    except Exception as e:
        msg = 'Missing configuration variable: {0}'.format(e)
        return jsonify({'error': msg})

    try:
        twilio_client.calls.create(from_=app.config['TWILIO_CALLER_ID'],
                                   to=phone_number,
                                   url=url_for('.outbound',
                                               _external=True))
    except Exception as e:
        app.logger.error(e)
        return jsonify({'error': str(e)})

    return jsonify({'message': 'Call incoming!'})


# Voice Request URL
@app.route('/sendMessage', methods=['POST'])
def sendMessage():
    # Get phone number we need to call
    phone_number = request.form.get('phoneNumber', None)
    message = request.form.get('message', None)

    try:
        twilio_client = TwilioRestClient(app.config['TWILIO_ACCOUNT_SID'],
                                         app.config['TWILIO_AUTH_TOKEN'])
    except Exception as e:
        msg = 'Missing configuration variable: {0}'.format(e)
        return jsonify({'error': msg})

    try:
        twilio_client.messages.create(
            from_="+15102963363",
            to=phone_number,
            body=message
            )
    except Exception as e:
        app.logger.error(e)
        return jsonify({'error': str(e)})

    return jsonify({'message': 'Message on the way!'})

@app.route('/outbound', methods=['POST'])
def outbound():
    response = twiml.Response()

    response.say("Thank you for contacting our service. We will connect you with a doctor right away...",
                 voice='alice')

    # Uncomment this code and replace the number with the number you want
    # your customers to call.
    with response.dial() as dial:
        dial.number("+15109968313")
        #dial.number("+16502743517")  Andy's Number

    return str(response)



if __name__ == '__main__':
    app.run(debug=True)

