from datetime import date

import httplib2
from apiclient import discovery
from oauth2client import file, client, tools
from apiclient import errors

flags = True


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    # This function generates the required credentials required to make
    # api calls
    SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
    store = file.Storage('credentials.json')
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        credentials = tools.run_flow(flow, store)
    return credentials


def get_label_id(service, user_id, label_name):
    """
    Return the label id of a Gmail label
    :param service: Authorized Gmail API service instance.
    :param user_id: User's email address. The special value "me"
    :param label_name: The name of the label id required
    :return: string(label_id)
    """
    label_id = ''
    try:
        response = service.users().labels().list(userId=user_id).execute()
        labels = response['labels']
        for label in labels:
            if label['name'] == label_name:
                label_id = label['id']
    except errors.HttpError as error:
        print('An error occurred: %s' % error)

    return label_id


def list_messages_matching_query(service, user_id, query=''):
    """List all Messages of the user's mailbox matching the query.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      query: String used to filter messages returned.
      Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

    Returns:
      List of Messages that match the criteria of the query. Note that the
      returned list contains Message IDs, you must use get with the
      appropriate ID to get the details of a Message.
    """
    try:
        response = service.users().messages().list(userId=user_id,
                                                   q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(
                userId=user_id, q=query, pageToken=page_token).execute()
            messages.extend(response['messages'])
        return messages

    except errors.HttpError as error:
        print('An error occurred: %s' % error)


def get_sender_email_id(service, user_id, msg_id, subject):
    """
    This functions return the email id of the sender
    :param subject: subject of mail
    :param service: The google service(here GMail)
    :param user_id: The user id of the user
    :param msg_id: The message id that is to be retrived
    :return: string(email id)
    """
    email_id = ''

    try:
        message = service.users().messages().get(userId=user_id, id=msg_id,
                                                 format='metadata').execute()

        header_data = message["payload"]["headers"]

        sender_text = "From"

        correct_subject = False

        for data in header_data:
            if 'subject' == data['name'].lower() and subject in data['value']:
                correct_subject = True

        if not correct_subject:
            return ''

        # Get email id from header data
        for data in header_data:
            if sender_text == data["name"]:
                email_id = data["value"]
                start = email_id.find('<')
                end = email_id.find('>')
                email_id = email_id[start + 1: end]
        return email_id

    except errors.HttpError as error:
        print('An error occurred: %s' % error)


def get_status_update_emails(status_update_date):
    """

    :param status_update_date: Date of the status update you want to query
    :return:
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    status_update_date_string = status_update_date.strftime('%d-%m-%Y')
    query = 'Status Update [%s]' % status_update_date_string

    emails = []
    messages = list_messages_matching_query(service, user_id='me', query=query)

    for message in messages:
        email = get_sender_email_id(
            service, user_id="me", msg_id=message['id'], subject=query)
        if email:
            # remove period from username part
            email_parts = email.split('@')
            email = email_parts[0].replace('.', '') + '@' + email_parts[1]
            if email not in emails:
                emails.append(email)

    return emails
