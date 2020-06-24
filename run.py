"""
Get all users from Auth0
"""
from datetime import datetime
import os
import pandas as pd
import boto3
from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0
from common import get_users_from_auth0


try:
    AUTH0_DOMAIN = os.environ["AUTH0_DOMAIN"]
    NON_INTERACTIVE_CLIENT_ID = os.environ["NON_INTERACTIVE_CLIENT_ID"]
    NON_INTERACTIVE_CLIENT_SECRET = os.environ["NON_INTERACTIVE_CLIENT_SECRET"]
    BUCKET_NAME = os.environ["BUCKET_NAME"]
except KeyError as e:
    print(e)
    raise ValueError("Environment variables not set")


if __name__ == "__main__":
    get_token = GetToken(AUTH0_DOMAIN)
    token = get_token.client_credentials(
        NON_INTERACTIVE_CLIENT_ID,
        NON_INTERACTIVE_CLIENT_SECRET,
        f"https://{AUTH0_DOMAIN}/api/v2/",
    )
    mgmt_api_token = token["access_token"]

    s3_client = boto3.client("s3")

    file_name = f'{datetime.today().strftime("%Y-%m-%d")}.csv'
    auth0 = Auth0(AUTH0_DOMAIN, mgmt_api_token)
    last_login = f'{datetime.today().strftime("%Y-1-1")} TO *'
    user_generator = get_users_from_auth0(auth0, last_login)

    # Keys within the dictionary returned by Auth0
    columns = ["name", "nickname", "user_id", "last_login", "logins_count", "email"]

    rows = []
    user_count = 0
    for user in user_generator:
        if "emails" in user:
            for address in user["emails"]:
                user["email"] = user["email"] + ", " + address["email"]
        if "github" in user["user_id"]:
            print(user_count)
            rows.append([user[column] for column in columns])
        user_count += 1

    df = pd.DataFrame(columns=columns, data=rows)
    df.to_csv(file_name)

    response = s3_client.upload_file(file_name, BUCKET_NAME, file_name)
