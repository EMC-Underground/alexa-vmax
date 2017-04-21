import logging
from rest_requests import RestRequests

LOG = logging.getLogger("flask_ask").setLevel(logging.DEBUG)

server_ip = ''  # ip of the Unisphere server to query
port = ''  # port to connect to the unisphere server on, e.g. 8443
username, password = 'smc', 'smc'  # credentials for the Unisphere server

base_url = 'https://%s:%s/univmax/restapi' % (server_ip, port)
vmax_req = RestRequests(username, password, False, None, base_url)

# HTTP constants
GET = 'GET'
POST = 'POST'
PUT = 'PUT'
DELETE = 'DELETE'


def check_status_code_success(status_code, response):
    """Check if a status code indicates success.

    :param status_code: the status code
    :param response: the server response
    """
    if status_code not in [200, 201, 202, 204]:
        LOG.error('Error making rest call. Response received is %(res)s'
                  % {'res': response})
        raise Exception


def get_array_list():
    """Returns a list of arrays.

    :return: array list
    """
    target_uri = "/84/system/symmetrix"
    response, status_code = vmax_req.rest_request(target_uri, GET)
    check_status_code_success(status_code, response)
    try:
        array_list = response['symmetrixId']
    except KeyError:
        array_list = []
    return array_list


def get_alert_summary(array):
    """Get a summary of alerts for a specified array.
    
    :param array: the array serial number
    :return: summary of alert information
    """
    perf_unacknowledged, array_unacknowledged, server_unacknowledged = 0, 0, 0
    target_uri = "/84/system/alert_summary"
    response, status_code = vmax_req.rest_request(target_uri, GET)
    check_status_code_success(status_code, response)
    server_unacknowledged = response['serverAlertSummary']['all_unacknowledged_count']
    symm_alert_list = response['symmAlertSummary']
    for symm_alert in symm_alert_list:
        if symm_alert['symmId'] == array:
            perf_unacknowledged = symm_alert['performanceAlertSummary']['all_unacknowledged_count']
            array_unacknowledged = symm_alert['arrayAlertSummary']['all_unacknowledged_count']
    return perf_unacknowledged, array_unacknowledged, server_unacknowledged


def get_all_array_alerts(array, filters=None):
    """Queries for a list of All Alert ids for the given array.

    Optionally can be filtered by: create_date_milliseconds(=<>),
    description(=<>), type, severity, state, created_date, acknowledged.
    :param array: the array serial number
    :param filters: dict of filters - optional
    :return: list of alert ids
    """
    target_uri = "/84/system/symmetrix/%(array)s/alert" % {'array': array}
    response, status_code = vmax_req.rest_request(target_uri, GET, filters)
    check_status_code_success(status_code, response)
    return response['alertId']


def get_alert(array, alert_id):
    """Queries for a particular alert.

    :param array: the array serial number
    :param alert_id: specific id of the alert - optional
    :return: dict, status_code
    """
    target_uri = "/84/system/symmetrix/%s/alert/%s" % (array, alert_id)
    response, status_code = vmax_req.rest_request(target_uri, GET)
    check_status_code_success(status_code, response)
    try:
        description = response['description']
        created_date = response['created_date']
    except KeyError:
        description, created_date = "Unknown", "Unknown"
    alert_desc = ("Alert description is %(desc)s. The alert was created on "
                  "%(date)s" % {'desc': description, 'date': created_date})
    return alert_desc


def acknowledge_array_alert(array, alert_id):
    """Acknowledge a specified alert.

    Acknowledge is the only "PUT" (edit) option available.
    :param array: the array serial number
    :param alert_id: the alert id - string
    :return: dict, status_code
    """
    target_uri = ("/84/system/symmetrix/%s/alert/%s" %
                  (array, alert_id))
    payload = {"editAlertActionParam": "ACKNOWLEDGE"}
    response, status_code = vmax_req.rest_request(target_uri, PUT,
                                                  request_object=payload)
    check_status_code_success(status_code, response)


def delete_alert(array, alert_id):
    """Delete a specified alert.

    :param array: the array serial number
    :param alert_id: the alert id - string
    :return: None, status code
    """
    target_uri = ("/84/system/symmetrix/%s/alert/%s" %
                  (array, alert_id))
    return vmax_req.rest_request(target_uri, DELETE)
