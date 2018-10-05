# gmail-cli-handler
Interact with your gmail account over the command line for quick batch operations. this currently only supports delete functionality by label or sender keyword.

## Setup

1. Follow the [python quickstart gmail API Docs](https://developers.google.com/gmail/api/quickstart/python#step_1_turn_on_the) to create a project, enable the gmail api, and download the credentials.

2. Rename the downloaded JSON file to credentials.json and copy it to the same directory as email_handler.py

## Run The Script

1. Navigate to the directory you copied the script to.

2. Run the script and add the input variables: <label> and <sender>. Label must be exact, but sender is a keyword search.
 
3. Ex: `$ python email_handler.py label='work' sender='myboss@msn.com'`

4. The script will open your browser to verify the OAUTH2 with the client and your gmail account.

5. Follow the command line prompst, the script will always ask before the final deletion of emails.

## NOTE
The gmail API does **not allow instant and total deletion**

This script **just moves emails to the trash folder**, which is cleared according to your settings

To allow instant and total deletion, you must submit a form to register your api with google,
since this can be a security issue/dangerous if not used properly.

## Resources

[python quickstart gmail API Docs](https://developers.google.com/gmail/api/quickstart/python#step_1_turn_on_the)

[builder API methods, handles all gmail interactions](https://developers.google.com/apis-explorer/#search/gmail/)

[gmail API http response types and query params](https://developers.google.com/gmail/api/v1/reference/users/messages#resource)
