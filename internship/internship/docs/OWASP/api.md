#OWASP TOP 10 API

Here lay my notes on the owasp top 10 api.

##Definitions

###Object

It describes information about a particular thing. A user object  might describe roles, names, usernames. A json object describes key-value pairs of information.

###Authentication

It's the process of proving who you said you were when you registered yourself . Tipically done by a username and password.

###Data

It's what information is made up of, data by itself isn't useful. When combined, it becomes information and is then useful.

###Resources

It's the intellectual/physical property of a certain thing, which can be used with a given purpose or not. In the context of web application, a resource can be a scroll page with articles.

###Rate-Limiting

It's how you throttle requests, by blocking them when you receive too many.

###Function 

It does a particular action. Its an operation

## OWASP API TOP 10

1. Broken Object Level Authorization - It happens when you are able to access an object which you should not have access to. There is nothing wrong with manipulating the id of an object, the problem arises when a given user has the permissions to access an object he should not have permissions to access. Eg: `/shop/user?id=1`

2. Broken User Authentication - Its any operation over authentication that allows an attacker to login as someone else. Eg: ` OR 1=1 --`

3. Excessive Data Exposure - Its the visualization of an object which is to sensitive to show but is perceivable by the users anyhow. Eg: `password` key-value pair in JSON body.

4. Lack of Resources & Rate Limiting - Its any operation that exceeds the maximum amount of resources a server can provide because there are no restrictions to how many the client can ask. Eg: `?limit=2000000`

5. Broken Function Level Authorization - Its any operation accessed by a user whose permissions should not allow him to access. Eg: `/admin/email?deleteEmailName=`

6. Mass Assignment - Its legitimate api calls that an attacker shouldn't have access to in any given endpoint. A user can set himself to admin, if an object in the backend exists that checks if the property admin is true, and the attacker sets it to true via the API. Eg: `"admin":true`

7. Security Misconfiguration - Its anything that is misconfigured to allow an attacker access to sensitive information or do sensitive operations. Eg: `redis`, `DELETE`  on unporposeful endpoint

8. Injection - Its anything that allows code or commands to be injected in a particular sink such as system in python, eval in js/php. Eg: `".phpinfo()."`

9. Improper-Assets-Management - Developers can't rewrite an API because they included new functionality code to the frontend, so they include new versions of their API and new endpoints towards those versions. An attacker can simply change the version of the api by changing the endpoint (v3 => v2), which could allow him access to older less secure features. Eg: `/v2/login/` => `/v1/login`

10. Insufficent Logging & Monitoring - The application does not log anything or few things and that means it won't be aware of any actions uninteded or intended, malicious or unmalicious that the client does.

##Vulnerable?

1.  If a user can access objects he does not have permissions to access, yes.

2. If there's a way a user can login as another user by exploiting a particular authentication vulnerability such as NoSQLi, SQLi, credential stuffing, then yes.

3. If an Object contains sensitive info that should not be shown and a user is able to see it, then yes.

4. If there is no restriction to the ammount of resources a user can ask, then yes.

5.  If a user is able to perform an operation he should not have access to, then yes.

6. If the user is able to legitemately manipulate the API to do things he should not do.

7. If there is somekind of misconfiguration that allows user access to sensitive information, then yes.

8. If user input goes to a sink which allows codes or commands to be injected, then yes.

9. If there's an older version of the api that an attacker can shift to, then yes.

10. If the application does not log or logs very few things, then yes.

##Char49 TIPS

###10 - Insufficent Logging & Monitoring

**Notice the lack of headers, body - In fact, there is no useful information that seems to be logged.**

###9 - Improper Assets Management.

**Remember old api endpoints don't necessarily have the same sub-endpoints.**

###8 - Injection

**Taking input directly to the terminal It is not the same as running a system function.**

###7 - Security Misconfigurations

**Disclosure of sensitive information can can result in mongodb database leak at port 27017, for example.**

###6 - Mass Assignment

**Can be used to bolster any type of privilege.**

###5 - Broken Function Level Authorization

**Operations that users aren't supposed to execute with their current authorization level**

###4 - Lack of Resources & Rate-Limit

**We can increase the limit value in the query string to increase stress on the server**

###3 - Excessive Data Exposure

**Rule of thumb: If it's not rendered and is in output, it should be excessive data exposure**

###2 - Broken User Authentication

**There are various techniques, but no rate-limit will surely lead to full account takeover. Analyze responses**

###1 - Broken Object Level Authorization
 
 **Notice the id change. We shouldn't have the authorization to see those, but we can see them**