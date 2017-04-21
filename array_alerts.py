import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import vmax_requests as vmax

app = Flask(__name__)
ask = Ask(app, "/")
LOG = logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def new_game():
    welcome_msg = render_template('welcome')
    return question(welcome_msg)


@ask.intent("YesIntent")
def list_arrays():
    arrays = vmax.get_array_list()
    len_array_list = len(arrays)
    arrays_msg = render_template('array', amount=len_array_list,
                                 array_list=list(enumerate(arrays)))
    session.attributes['arrays'] = arrays
    return question(arrays_msg)


@ask.intent("ChooseArrayIntent", convert={'index': int})
def choose_array(index):
    array_list = session.attributes['arrays']
    try:
        array = array_list[index]
    except IndexError:
        msg = render_template('indexerror')
    else:
        session.attributes['array'] = array
        (perf_unacknowledged, array_unacknowledged,
         server_unacknowledged) = vmax.get_alert_summary(array)
        total_unacknowledged = perf_unacknowledged + array_unacknowledged + server_unacknowledged
        if total_unacknowledged:
            msg = render_template('alerts', array_alert_num=total_unacknowledged,
                                  server_unacknowledged=server_unacknowledged)
        else:
            msg = render_template('no_alerts')
    return question(msg)


@ask.intent("ListAlertsIntent")
def list_and_acknowledge_alerts():
    return_alerts = []
    array = session.attributes['array']
    alert_list = vmax.get_all_array_alerts(
        array, filters={'acknowledged': 'false'})
    if alert_list and len(alert_list) > 0:
        for alert_id in alert_list:
            alert_details = vmax.get_alert(array, alert_id)
            return_alerts.append(alert_details)
            vmax.acknowledge_array_alert(array, alert_id)
    msg = render_template('alert_details',
                          alert_list=list(enumerate(return_alerts)))
    return question(msg)


@ask.on_session_started
def new_session():
    LOG.info('new session started')


@ask.intent("GoodbyeIntent")
def goodbye():
    return statement(render_template('goodbye'))


if __name__ == '__main__':
    app.run(debug=True)
