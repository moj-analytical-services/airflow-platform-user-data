# Auth0 Platform User Data

##### Query Auth0's API and export data in csv format to an S3 bucket

### Prerequisites

- OIDC Client ID
- OIDC Client Secret 
- S3 Bucket

You'll need to have an auth0 [application](https://auth0.com/docs/applications) in order to retrieve these values

**Note**

This app requests temporary credentials every time it executes.  You'll need to ensure the resulting bearer tokens have the following scopes

- `create:client_grants`
- `read:client_grants`
- `read:connections`
- `read:users`


#### Write to S3

```bash
export AUTH0_DOMAIN="alpha-analytics-moj.eu.auth0.com"
export NON_INTERACTIVE_CLIENT_ID="41Tmoz00wBN1..."
export NON_INTERACTIVE_CLIENT_SECRET="StdNYnUaPuv9iMEfKsiLEZ0GUTe...."
export BUCKET_NAME=my-auth0-bucket
```


### Configuration

| Env Variable  | Default  | Description                                |
|---------------|----------|--------------------------------------------|
| `CLIENT_ID` | (**Required**) | The Client ID of the auth0 application used for this app |
| `CLIENT_SECRET` | (**Required**) | The Client Secret of the auth0 application used for this app |
| `AUTH0_DOMAIN` | (**Required**) | Auth0 management API endpoint |
| `BUCKET` | (**Required**) | The `S3` bucket to write to. 
