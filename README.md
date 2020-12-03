# post-checker
This  program was originally written to check automatically the website on which a list of people
who received packages in my building is posted. It can be used as a notification tool for any
website which you want to check regularly. It works by downloading the website content and looking 
for a match for a given string (in the case of the package list this is simply my name). 
If a package has arrived an email is sent using the Gmail API. Note: this could have been done 
with sendmail, but using the gmail API only requires the http protocol. Indeed the SMTP
protocol is blocked in my building.

## Classes

### PostChecker
The class `PostChecker` has a method 
`check_post` which returns `True` if a given string is found on the website and `False` otherwise.

### Mail

The class `Mail` takes a sender, a subject, a recipient and a message text as inputs, creates a 
message through the method `create_message` and sends it with the method `send_message`. 

For authentication a credentials.json file is required, which you can get by enabling the Gmail API on
https://developers.google.com/gmail/api/quickstart/python . You will then be required to enter your password the first time you
run the program.

