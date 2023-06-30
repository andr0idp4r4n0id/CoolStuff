#Writeup c{api}talctf 

**This ctf is a training done by checkmarx to introduce people to API hacking in a gentle way. Kudos. Checkmarx.**

##Definitions

###Functional View - What is it?

__This form of recon ascertains the functionality of the web app. For example, what is the website's purpose?  Does it have login capabilities? If so, can I register an account? What can I do upon logging in? This is a very important phase of the recon process. You won't break anything if you don't understand how it was built.__

###Technological View - What is it?

__This is the next phase after the functional view of the recon process. Purposefuly made to acquire information related to technology. Which server hosts the app? Is there a framework linked to that? What ports are open? Is it the same server running on that port? Does it have an API? What's the backend language?__

###OSINT View - What is it?

__This is my final phase of the recon process. It's about researching of the technologies and functionalities discovered before. If it's using FastAPI, for example, are there any default config, db, env files? Basically, google to find open source intelligence information about my discoveries.__

##Recon

 __localhost:4100__

###Functional View

**Home Page**

The main page is a feed with posts from various different users.
Tags will filter the posts. 
Reading every post is very important to attain information.
By clicking on the `Dev Updates #4`, I read there are unsecured endpoints. (DevOps and Administrative endpoints).
After clicking on the post `I am Pikachu!`, I see there is an email: `Pikachu@checkmarx.com`.

**Sign up Page**

In order to sign up, I need a `username`, a `email`  and a `password`. I create my account and it automatically logs me in.

**Settings Page**

It allows me to set an image, change my username, email, password, set a bio and logout.

**New Post Page**

It allows me to create an article which is composed by a `title`, `summary` , write an article in `markdown` and add tags which can be used for filtering purposes.

**My Profile Page**

It simple shows my articles and favorited articles.

###Technological View



The most common way to acquire technology information about the target is to analyze headers and produce errors. Maybe a null byte (It's keen to a stop sign. It will stop, in this case, the processing of the string), in the url will produce a 500 that leaks information about the backend? A simple head request could return a `Server` header. It is important to emphasize that the information can be faked. It is the responsability of the researcher to understand what is true and what is not.

Curling the root of the url,  `http://localhost:4100/`, the `X-Powered-By` header is present with a value of `Express`. This means javascript could be running on the backend of the server at port 4100.
To confirm that, I open the source code, since there could be another hint to another backend server. Nothing hints at another server but an interesting file is found: `http://localhost:4100/static/js/bundle.js`

I take note of it and continue curl a page I knew did not exist: `http://curl -I localhost:4100/123`
The same header is present.

I run an nmap to find which ports are open that server: `nmap -sS -sV -p- --min-rate=500 localhost`. This scan basically initiates a connection and ends it halfway, discovering if the port is open or not, due to the server's response halfway through the connection.
There are various ports open but the one which interests me more is `8000` and `6379`

###OSINT View

I start googling for sensitive files express could have. (Config files, env files, db files, etc). But quickly find out most of express's configuration is done via the terminal, and that express is simply a framework to create web applications and apis, and as such does not come with default configuration files that you can access via the http protocol.



__localhost:8000__

###Functional View

The nmap scan shows us it's an http server, therefore it can be opened in a browser. It returns a `404` status code, implying there is no route for `GET` at `/`. Going a step back, I re-opened the application at `4100` and opened up BurpSuite. (It's an application which allows me to "grab" or intercept a network request, edit it, and then send it off again.). With intercept mode on, I login and see it makes a request to the same host at port `8000`on an endpoint `/api`. 

This means the frontend (blog) communicates with the backend through the API. Everything goes to the API before going to the backend. 
The though process now is to use the functionalities of the web application, whilst intercept is on, to see how communication is done with the API.

By clicking on the homepage, I see it makes a request to the same server at port 8000 on the endpoint `/api/articles?limit=10&offset=0`
So it may not be a paged file but instead a scroll file. The limit is the maximum ammount of articles which can appear and the offset is from which article to show.

By clicking on my profile I see it makes a request to `/api/profiles/android` and that shows interesting json attributes: `admin`, `cardName`, `cardNumber`, `cardCvc`, `cardExpiry`

Updating my profile sends a `PUT` request to `/api/user/` with a json body.

By creating an article I see it makes a `POST` request to `/api/articles` with a json body again.

Cicking on a post sends a `GET` to `/api/articles/<post_name>`

Taking into account the requests it just made to the API, I can conclude it is using an API of type REST, because it's using the whole of the http protocol to communicate throughout different endpoints.

###Technological View.

Curling with a head request at `http://localhost:8000` , I see it uses a server called `uvicorn`. 

Another curl head request to a 404 directory on that server: `http://localhost:8000/123`. It also shows uvicorn.

###OSINT View

After googling what uvicorn is, I see its a python based server for the ASGI specification. Its basically an asynchronous web server. It can use various API frameworks.

After googling for specific endpoints for each framework, I find one that returns a 200. It is `/docs`. It simply compiles the information from `openapi.json` into a more familiar and readable format. To be truthful, `/docs` is a very common endpoint, but, in this case, means the framework is utilizing `FastAPI`.


##Exploitation

###First Flag

Whilst analyzing the docs, I notice an admin attribute at `/api/user`. This means, according to the API, there is an attribute `admin` linked to the backend code, which, when set, will make me `admin`. Basically, logically speaking, somewhere in the backend, there is a conditional check keen to: `if(user.admin) { admin stuff }`.
Go to settings page of the frontend. Click update settings with intercept on. 

Write in json format the following json key-pair value: `"admin":true` to the body of the json request. Send it off. You are now `admin`

The flag is: `flag{M4sS_AsS1gnm3nt}` - Belongs to: **Mass Assignment**

Do not let the user change its own role, especially to roles with higher privileges.

###Second Flag
The next endpoint at the docs which seems interesting is the `/api/debug/` endpoint. By the looks of it, it sends a command, by default, `uptime` to the server. It is a linux command, which implies that, most likely, since its python, there is a system function call with user input in it. We can injection arbitrary shell functions then. See it as a connection between your computer and the API. Everything in that input will be seen by the computer as a command.
Copy the default body from `/docs` and paste it onto the repeater. Replace `uptime` with  `uptime; ls;`  and a flag is received. It is:
`flag{1nject10n_Ap1}` - Belongs to: **Injection**

Do not use the system function. More clearly, do not send user input to functions which allow execution of commands.
****
###Third Flag
Taking a peak at the docs, I see endpoints, which, when receiving a `DELETE` request, will delete an article or comment. The thought process here is, according to the logic of the application, that a normal registered user shouldn't be able to delete other user's privilege. An admin? Sure. But a regular user? Is it really necessary to allow a regular user to delete other's comments and articles?. Stop being admin by sending a `PUT` request to `/api/user` but with admin set to false. (Like we did the last time, intercept the request at `/settings` and add a json attribute like: `"admin":false`). It allows the request and deletes the article. This means that in the backend there is code which does not validate the permissions correctly. Maybe the `regular-user` and `admin-user` classes both inherit from `User` and it was forgotten to unvalidate some permissions? Re-devoloping the code isn't a good idea. You can simply check if a user is admin, and if so, allows the request to delete other user's articles and comments. If not, it only allows to delete his own articles.
The flag is: `flag{B0lA!!!!!}` - Belongs to: **Broken Object Level Authorization**

###Fourth Flag

There's another port open. It is: `6379`. It's hosting redis, a database. Redis-cli is a command line program to communicate with it. Simply open a terminal, write `redis-cli -h 127.0.0.1` and notice a database shell opens. Redis uses keyspaces to enumerate existing db's. That is, keyspace 0 means there is a db 0. To do that, write `INFO keyspace`. It will output the number of the database you need to select. Take into account this is only possible because there is no user authentication. The security misconfiguration happens because an attacker can interact with the server without authentication.

Write `SELECT 0` and enumerate all the keys with `KEYS *`. There's one called flag. Get it with `GET flag`. The flag is: `flag{5eC_M1sc0nF1g}` - Belongs to: **Security Misconfiguration**

###Fifth Flag

If you provide a way to associate sentitive info with a profile, do not show that sensitive info in the API or frontend. Keep it in the backend. And if you do decide to show it, show only to the current user.
Noticing the user's profile's returns card info, and that one user told he was giving away money, I concluded he had associated his card info. As such I did a `GET` to `/api/profiles/TeamR$cket` and there it was, his credit card info. I remembered the membership options and decided to test his card there. It worked a flag popped up. It is: `flag{3xc3ss1v3_daTa_Xp0sur3}` - Belongs to: **Excessive Data Exposure**

###Sixth Flag

Most users re-use passwords and use passwords with personal information. In this case, the user Pikachu made a post with his favorite pokemons. Deductive reasoning led me to believe it could be one of his passwords. After placing the pokemon list on intruder and attempting each one to login, the last one let me in. The password is `snorlax` and the flag is: `flag{br0k3n_uS3r_4uthEnt1cAt1oN}` - Belongs to: **Broken User Authentication**

Locking the account after 3-5 failed login attempts should fix this. You can't allow a user to bruteforce his way through your login system, as that will lead to a broken authentication system.

###Seventh Flag
After logging on Pikachu, we can see there's a logging endpoint. We test it on the frontend and a message is displayed saying there is no logging or monitoring. We test it on the backend/API and we get a flag: `flag{InsUfF1C3nT_L0gG1nG}` - Belongs to: **Insufficient Logging**

Lack of logging is problematic. You want to know who logged in and where, who takes action `X` or not. Logs are important to keep track of everything that happens in the application.

###Eighth Flag
There's a post by Hodor which says there are administrative endpoints. We test it on the frontend with `/admin/` and it is deprecated. We test it on the backend/API with `/api/admin` and we get a flag! `flag{BFL4_I_aM_Th3_aDm1n_H3r3!}` - Belongs to: **Broken Function Level Authorization**

A normal user should not be allowed to access administrative endpoints, the backend code needs to make a check which looks at the user's roles and see's if it has the necessary ones to enter an admin endpoint: `if(user.admin) { allow } else { do not }`

###Ninth Flag

Scrolling pages need to have a defined limit, a maximum number of articles, in this case, that it shows. Otherwise you can stress the database by asking too many, leading to a DoS.

 The limit parameter, in this case, we can change it to `200000` and we provoke rate-limiting issues and thus we get the flag: `flag{L4cK_0f_R3s0urc3S_&_r4t3_L1m1t1ng}` - Belongs to: **Lack of Resources & Rate-Limiting**

###Tenth Flag

Developers often need to re-write parts of an API because they add new functionality to the frontend and need a way to communicate with the backend. Thus leading to a new directory, for example, `v3` with the updated API. Forgetting to forbid access to the lower API versions could lead to security risks, as unpatched API is more prone to security issues and misconfigurations.
Improser-Assets-Mangement, we can see the login endpoint has a v2. We attempt to use v1 and login. It works and the flag is there. It is: `flag{Impr0peR_Ass3ts_ManAg3m3nt}` - Belongs to: **Improper Assets Mangement**








 














