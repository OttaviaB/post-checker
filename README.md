# post-checker
This  program was originally written to check auotmatically the website on which a list of people
who received packages in my building is posted. It can be used as a notification tool for any
website which you want to check regularly. It works by downloading the website content and looking 
for a match for a given string (in the case of the package list this is simply my name). 
If a package has arrived an email is sent using the gmail API. Note: this could have been done by 
using sendmail, but using the gmail API only requires the https protocol. Indeed the sendmail 
protocol is locked in my building.

## Classes

### PostChecker
The class `PostChecker` has a method `get_html` for downloading the website content and a method
`check_post` which returns `True` if a given string is found on the website and `False` otherwise.

### Mail

The class `Mail` takes a sender, a subject, a recipient and a message text as inputs and creates a 
message through the method `create_message` and sends it with the method `send_message`. Authentication
is done when initialising a class object and is required only the first time.
