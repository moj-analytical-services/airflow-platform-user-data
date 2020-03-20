from auth0.v3.management import Auth0
import math


def get_users_from_auth0(auth0_conn: Auth0, last_login):
    """
    Get all users from Auth0

    :param auth0_conn: Authenticated Auth0 API client
    :param regex: Regex to filter users (re.match(user.email))
    """

    t = last_login
    query = f'last_login:[{t}]'

    users_list = auth0_conn.users.list(q=query)

    total_users = users_list['total']
    page_size = users_list['length']

    # don't waste the first request
    for u in users_list['users']:
        yield u

    del users_list

    # iterate through subsequent pages
    for page in range(1, math.ceil(total_users / page_size)):
        for u in auth0_conn.users.list(page=page,
                                       q=query)['users']:
            yield u
