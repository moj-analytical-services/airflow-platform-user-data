from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0
from datetime import datetime
from common import get_users_from_auth0
import pandas as pd
import boto3
import os

try:
    auth0_domain = os.environ['AUTH0_DOMAIN']
    non_interactive_client_id = os.environ['NON_INTERACTIVE_CLIENT_ID']
    non_interactive_client_secret = os.environ['NON_INTERACTIVE_CLIENT_SECRET']
    bucket_name = os.environ['BUCKET_NAME']
except KeyError as e:
    print(e)
    raise ValueError("Environment variables not set")


if __name__ == "__main__":
    get_token = GetToken(auth0_domain)
    token = get_token.client_credentials(non_interactive_client_id,
                                         non_interactive_client_secret,
                                         f'https://{auth0_domain}/api/v2/')
    mgmt_api_token = token['access_token']

    s3_client = boto3.client('s3')

    file_name = f'{datetime.today().strftime("%Y-%m-%d")}.csv'
    print(file_name)
    auth0 = Auth0(auth0_domain, mgmt_api_token)
    last_login = f'{datetime.today().strftime("%Y-%m-%d")} TO *'
    user_generator = get_users_from_auth0(auth0, last_login)

    # Keys within the dictionary returned by Auth0
    columns = ["name", "nickname", "email", "user_id",
               "last_login", "logins_count"]

    rows = []
    user_count = 0
    for user in user_generator:
        rows.append([user[column] for column in columns])
        user_count += 1
        if user_count == 300:
            break

    df = pd.DataFrame(columns=columns, data=rows)
    df.to_csv(file_name)
    response = s3_client.upload_file(file_name, bucket_name, file_name)
