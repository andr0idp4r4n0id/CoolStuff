# SAML

## What is it

**It allows access to multiple websites with only one set of login credentials**. It's based on **XML**. The user is authenticated by sending his login credentials to an **idP** (identity provider), which responds with a saml request that is sent to the browser, and from there the saml request is sent and validated by the **sp**.

## Flow

1. user accesses sp which uses idp for authentication
2. web app responds with a saml request
3. browser forwards saml to the idp
4. idp parses/authenticates the user
5. idp sends request to browser again
6. browser sends generated saml to sp
7. if saml is verified, access is granted

### Important

**I can hijack a user's session if I capture the token sent to the sp for validation**

## Attacker's Perspective

Timestamp - **Messages can be expired or not, and we can tamper with that.**

Assertion unique ID - **Only one session should be opened with the unique ID. If more than one is allowed, we can use the session at the same time the user operates it.**

Self Signed Certificates - **We can clone the original one or self sign our own**

Missing signatures - **Allow tampering with permissions in sp**

SAML recipient differ - **Allows an application user to login to other application. As an attacker this means compromising app A can lead to compromising app B.**


``` 

XSW - Behavior from multiple signatures/assertions

XSW 1 - Unsigned copy of the response after signature

XSW2 - Same but before signature

XSW 3 - Copy of assertion before signature

XSW 4 - Copy of assertion after signature

XSW 5 - Change value of original assertion, add copy of original assertion without signature at the end of saml response.

XSW 6 - Change value of original assertion, add copy of original assertion without signature after the original signature

XWS 7 - Add extension block

XSW 8 - Add object block.

```

## Exploiting

**Change expiration**

**Modify Parameters**

**XSW**

**Attempt to create a valid signature**

## References

https://cwe.mitre.org/data/definitions/287.html

https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/

https://cheatsheetseries.owasp.org/cheatsheets/SAML_Security_Cheat_Sheet.html

## Damn Vulnerable SAML Application

The idp server runs at 127.0.0.1

The sp server runs at 127.0.0.1:8000

There's a single logout feature

The application allows to change default security configurations like the message and assertion encryption/signing

The application has the following exploit scenarios: escalate privileges, employ XSW, use a self sign certificate, remove signing, change timestamps, XXE and XST

This can all be done as according to any other SAML configuration via a burp extension: SAML Raider.

### Scenarios

- No security configuration
- Valid Assertions/Messages
- Messages/Assertions signed
- Messages/Assertions signed and valid

1. No security configuration:

Without security configuration, it is possible to edit the saml response in anyway we can. To escalate privileges, we can simply change the `memberOf` attribute in the `SAML` response to `administrators`.

After accessing the `complaints` tab, the gui should allow us to delete users.

2. Valid Assertions/Messages:

The configuration wants valid assertions and messages, but only checks if they are valid if a signature exists. This means removing the signature permits editing the assertions and escalating our privileges.

After removing the signature in `SAML Raider`, change the `memberOf` attribute to `administrators`. Access the `complaints` tab and the GUI should allow deletion of complaints.

3. Messages/Assertions Signed

In this situation, the application checks that the `SAML` is signed, but it does not validate the assertion. An attacker can edit the assertion and change the group membership by editing the `memberOf` attribute to `administrators`.

4. Messages/Assertions signed and valid.

In this application, the only bypass is by leveraging `CVE-2017-11427`. This CVE plays with the parsing of the XML to trick the application into thinking we did not alter anything in the SAML response, but in fact we did. We can do this by adding a comment to the `memberOf` attribute after administrators:

`administrators<!--butnot-->`

## SAML Raider

It automates XSW attacks, attempts XXE and XST, allows inserting custom self signed certificates and remove signings.



