# alexa-vmax
Sample Python app to get started on connecting an Alexa device to a VMAX. Initial functionality allows you to choose one of the arrays in your environment and query for any alerts. A Unisphere server (running version 8.4) is required.

# Setup and testing
1. Install requirements
Ensure you have Python installed. Using pip, install Flask-Ask (pip install flask-ask).
Install ngrok (a command-line program that opens a secure tunnel to localhost and exposes that tunnel behind an HTTPS endpoint) and unzip (https://ngrok.com/download).

2. Grab the code
You can clone this repository. To configure the code for your own environment, edit lines 6 and 7 in the vmax_requests file to reflect your own Unisphere server details.

3. Run the program and expose the endpoint
In terminal, type "python array_alerts.py".
In a new terminal, cd into the location of ngrok and type "$ ./ngrok http 5000 " on Unix/Mac/Linux or "ngrok.exe http 5000" on windows.
Make a note of the HTTPS endpoint which is forwarding to localhost:5000 (e.g. https://20ba2c6f.ngrok.io ).
The localhost must be able to contact the Unisphere server.

4. Configure the Alexa skill
Make sure you're logged into your Amazon developer account, and go to your list of Alexa skills. Click the "Add a New Skill" button. Configure each section as outlined below:

- Skill Information Settings
Leave the "Skill Type" set to "Custom Interaction Model"
Enter "Array Alerts" (without quotes) for both the "Name" and "Invocation Name" fields.

- Interaction Model Settings
Copy the contents of the intent_schema.json into the "Intent Schema" field. Don't worry about "Custom Slot Types".

Copy the statements below into the "Sample Utterances" field:

YesIntent yes

YesIntent sure

ChooseArrayIntent {index}

ListAlertsIntent alerts

ListAlertsIntent alert

GoodbyeIntent no

GoodbyeIntent goodbye

GoodbyeIntent bye

- Configuration Settings
Make sure the HTTPS radio button is selected for the "Endpoint" field.
Enter the HTTPS endpoint from ngrok into the textfield.
Don't bother with "Account Linking".

- SSL Certificate Settings
It's important to choose the second radio button with the label because that's what ngrok uses: 
"My development endpoint is a subdomain of a domain that has a wildcard certificate from a certificate authority."

We don't need to go through any other screens. Simply make sure the information on all sections above are saved.

5. Testing the skill
You can test the skill using any Alexa-enabled device associated with your account, using the interactive text prompt in the app portal, or using EchoSim.io .
Try the following sequence to test the app:

You - "Alexa, start array alerts"
Alexa - "Welcome to VMAX Alexa. I am going to list out the arrays in your environment. Ready?"
You - "Yes"
Alexa - "There are two VMAX arrays in your environment. These are 0: '000197800128', 1: '000296800647'.
       Select an array by stating its corresponding position in the list.
       Which array would you like to query?"
You - "Zero"
Alexa - "The details of the selected alerts are as follows: 0. Alert description is (blah blah). The alert was created on (blah blah). 
         1. Alert description is (blah blah). The alert was created on (blah blah). Would you like to choose another array?"
You - "No"
Alexa - "Goodbye and thank you."


See https://developer.amazon.com/blogs/post/Tx14R0IYYGH3SKT/Flask-Ask-A-New-Python-Framework-for-Rapid-Alexa-Skills-Kit-Development 
