## Browser Security

## Vulnerability Identification
The web application you have cloned makes use of a third-party advertisement network to monetize the site’s content.

vulnerability/tmpl/index.html 
src.postMessage(data, '*');

postMessage is injecting client side vulnerability
Sender can specify '*' instead of an actual origin - Any frame can receive the message 

The postMessage API is an HTML5 extension to allow secure cross-frame messaging - Sending a message is only possible if a frame handle can be acquired.Browser ensures that the receiver has the expected origin. Receiver origin is speciﬁed in the postMessage call - Receiver must check the sending origin but in this case its not checked which is causing cross frame messaging 

Syntax for postMessage:

otherWindow.postMessage(message, targetOrigin, [transfer]);

## Exploit the Vulnerability
The postMessage() method was created to enable cross-document messaging from applications on separate domains
Wihen tried to leak the value of document.secret on the server side its value is undefined.

## Proof concept 
Let's take the following example:
If Site amplifier wants to read content from Site modulator using a script like this:

Site amplifer snippet:
"iframe src="http://modulator.net/" name="modulator"

script
document.getElementsByName('modulator')[0].onload = function() {
    frames[0].getElementById("Evil").innerHTML = "SVS";
}
/script
"
Site modulator:
div id="Evil">/div

It would receive a same-origin error saying "Error: SecurityError: Blocked a frame with origin 'http://amplifier.com' from accessing a cross-origin frame."  

## PostMessage: postMessage() method, we can avoid this error by using the following code:

Site amplifier:

"button onclick="frames[0].postMessage('SVS','*')"Send Message/button

Site modulator:
div id="Evil"div

script
window.addEventListener('message', writeMessage, false);
function writeMessage(event) {
    document.getElementById("Evil").innerHTML = event.data;
}
script
Which would result in Site amplifier sending the message "SVS" to Site modulator and writing it to the DOM .


postMessage() method allows us to communicate between iframes, we essentially have created a new attack vector for exploiting XSS

Because Site modulator is actively listening for any site to send it a message, the attacker can load Site modulator as an iframe in an evil webpage that he controls, Site y.

Now he can send a malicious XSS message to Site modulator using the postMessage() method:

Code snippet:
button onclick="frames[0].postMessage('<img src=p onerror=alert(document.cookie)','*')"Attackbutton

Malicious message was sent from the attacker controlled webpage to Site modulator, then was written to the DOM and executed as javascript. This resulted in the alert box containing the session id.  


## Patch the Vulnerability:

There are ways securing the postMessage() method. 
Specifically designate the target origin when sending messages to another application. 

frames[0].postMessage('Evil','http://modulator.net');

Receiving side, all listeners should verify the event.origin parameter before accepting any messages

if (event.origin == "http://amplifier.com") {
	---------------
}else{
	---------------
}


## Harden the Application

CSP is a browser security framework proposed by Sterne at Mozilla in 2008 - Originally intended as an all-encompassing framework to prevent XSS and CSRF - Can also be used more generally to control app/ extension behaviors - CSP allows developers to specify per-document restrictions that override the SOP 
Ex:
Given in the header of the HTML with meta tag which must contain content.
meta http-equiv="Content-Security-Policy" content="frame-src 'self'"/>

Ex 1:
A server wishes to load resources only form its own origin:
Content-Security-Policy: default-src 'self'

Ex 2:
An auction site wishes to load images from any URI, plugin content from a list of trusted media providers (including a content distribution network), and scripts only from a server under its control hosting sanitized ECMAScript:

Content-Security-Policy: default-src 'self'; img-src *; object-src media1.example.com media2.example.com *.cdn.example.com; script-src trustedscripts.example.com

Ex 3:
banking site wishes to ensure that all of the content in its pages is loaded over TLS to prevent attackers from eavesdropping on insecure content requests:

Content-Security-Policy: default-src https: 'unsafe-inline' 'unsafe-eval'

 http-equiv="Content-Security-Policy" content="frame-src 'self' http://modulator.ccs.neu.edu"/>
 http-equiv="Content-Security-Policy" content="img-src 'self'"/>
 http-equiv="Content-Security-Policy" content="font-src 'self' http://fonts.googleapis.com http://fonts.gstatic.com"/>
 http-equiv="Content-Security-Policy" content="object-src 'self'"/>






