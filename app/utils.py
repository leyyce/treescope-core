jwt_authorizations_doc = {
    'jwt_header': {
        'type': 'apiKey',
        'name': 'Authorization',
        'in': 'header',
        'description': "JWT Bearer token. Use 'Bearer {your-token}' format in the Authorization header."
    }
}


def message(status, msg):
    response_object = {'status': status, 'message': msg}
    return response_object


def validation_error(status, errors):
    response_object = {'status': status, 'errors': errors}

    return response_object


def err_resp(msg, reason, code):
    err = message(False, msg)
    err['error_reason'] = reason
    return err, code


def internal_err_resp():
    err = message(False, 'Something went wrong during the process!')
    err['error_reason'] = 'server_error'
    return err, 500
