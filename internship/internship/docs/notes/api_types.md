#API Protocols

##Glossary

###RPC

###What is it?
Remote Procedure Call - It's a way of asking for services from one program to another remotely. The client requests and the server provides, 

###Internals of RPC

Basically, the input parameters are passed to the RPC. They parameters may not be raw, as certain data types may have different representations varying from machine to machine. The remote host executes the RPC after the parameters arrive. When an RPC program is called, it uses portmap to bind itself to a port, and the remote machine's RPC also contacts portmap to find the corresponding port number it needs to call the procedures by the application that asked to call them. The RPC program is assigned an integer identifier known only to those who will call its procedures. They are also assigned an integer number. That's how the remote RPC know what to call.

###Logic process of an RPC.

The RPC is called client side => parameters and the method to be called are marshalled => data is sent over over established ports known to both of the parties => data is unmarshalled server side => data is executed server side => return value is sent to client side.


##Rest

###What is it?

**Rest** is an api protocol that uses the entirity of http protocol to perform what it needs to do. It utilizes the verbs, headers, various endpoints.

If I see an API that uses the verb `DELETE` in an endpoint to erase an account, and a `GET` to fetch it in another endpoint, than I immediatly know it is using **REST**

As per good practices, the verbs have methodologies:

The `GET` retrieves a resource

The `PUT` changes the state or updates a resource.

The `POST` creates a resource

The `DELETE` removes it.


**Vulnerabilities** arise mostly when there are misconfigurations in these things. For example, if an application uses `DELETE` to erase an email, which means, to erase a resource, how would it react to erasing resources that should not be erased? Eg: `GET /profile` => `DELETE /profile`. Divergencies can also be  a root cause. If, for example, there's an `admin` attribute in a `User Class` and a normal user can set that to true, either by updating the resource or creating a new one, then there is cause for alarm.  In my opinion all vulnerabilities in API walk hand in hand, that is, for example, you normally can't do credential stuffing (BUA) if there is a rate-limit check in place. If you access an admin behaviour that allows you to enumerate the `User` Object, then you also have a BOLA and not only a BFLA. It's important to consider that one vulnerability can lead to another. Creativity is key in these thought processes.  The obvious point is that you can only be creative if you pay attention to all the details. Maybe the BFLA reflected in the logs and you can get a log injection. Otherwise, it could have been sent to a database and you can get an SQLi. 

Most representations of the REST requested resource will be JSON or XML.

Resources should be uniquely identifiable from a single URL.

Operations must be stateless, and any state necessary shall be done in the client

All resources should allow caching, unless explictly indicating caching is not possible.

###EXAMPLES OF REST REQUESTS.

`GET /api/user/messages HTTP/2`

-----------
```
POST /api/user/messages
<headers>

{
	"message_1": "Hello"
}
```

**Useful Link**: `https://hackerone.com/reports/384782`

##SOAP

###What is it?

**SOAP** Relies heavily on XML - every operation provided by the service is explicitly written in XML and received back in the same format. Each input parameter is bound to a type. This all codified in WDSL, which is used to describe the functionality of a webservice.

A **SOAP** request is composed of the following:

1. `soap:Envolope` - Describes the XML as SOAP type.

2. `soap:Header` - Is able to load SOAP modules

3. `soap:Body` - Bulk of the SOAP message (payload)

4. `soap:Fault` - For error messages.

Only `soap:Envolope` and `soap:Body` are actually required.

**Vulnerabilties** arise from improper usage of the input supplied within the SOAP request. These can be: **Injection( SQli, CMDi, XAML)**, **XXE**, **MitM by SOAP action spoofing**, **XSS**, **Broken Access and Authorization**, **DoS**

###Example SOAP REQUEST

```
<?xml version="1.0"?>

<soap:Envelope
xmlns:soap="http://www.w3.org/2003/05/soap-envelope/"
soap:encodingStyle="http://www.w3.org/2003/05/soap-encoding">

<soap:Body>
  <m:GetUserResponse>
    <m:Username>Tony Stark</m:Username>
  </m:GetUserResponse>
</soap:Body>

</soap:Envelope>

```
**Useful Link**: `https://hackerone.com/reports/36450`

##JSON-RPC

###What is it?

**JSON-RPC** means all the requests are made through JSON onto a single page. These can call specifc methods and params to that, along with an ID. The response is usually composed by a result object, error object and an id.

**Useful Link**: `https://hyperchain.readthedocs.io/en/latest/JSON-RPC_manual.html`

###Example JSON-RPC

```

--> {"jsonrpc": "2.0", "method": "subtract", "params": {"minuend": 42, "subtrahend": 23}, "id": 3}
<-- {"jsonrpc": "2.0", "result": 19, "id": 3}

```

**Useful Link**: `https://hackerone.com/reports/303390`

##XML-RPC

###What is it?

**XML-RPC** Utilizes the HTTP protocol and the POST method to pass a XML document contained in the body. Based on that, it generates the parameters for the function code to be executed and sends a response back in XML with the return value.

It supports the following datatypes:

```
Data type 	Tag example 	Description
array 	<array><data>…</data></array> 	A list that can contain multiple values or data types
base64 	<base64>SGFsbG8gV2VsdA==</base64> 	Base64-encoded binary data
boolean 	<boolean>1</boolean> 	Boolean variable (true = 1 vs. false = 0)
dateTime.iso8601 	<dateTime.iso8601>20200414T16:23:55</dateTime.iso8601> 	Date and time in ISO 8601 format
double 	<double>-0.32653</double> 	Double precision floating point number (64-bit)
integer 	<int>32</int> or <i4>32</i4> 	Integer (whole number)
string 	<string>Hello world!</string> 	String of characters; can contain zero bytes
struct 	<struct><data>…</data></struct> 	Set of key-value pairs (keys in this case are character strings and values can be any type) 

```
###Example XML-RPC

```

<struct>
  <member>
    <name>entry 1</name>
    <value><int>1</int></value>
  </member>
  <member>
    <name>entry 2</name>
    <value><int>2</int></value>
  </member>
</struct>

```

**Useful Link**: `https://hackerone.com/reports/500515`


##gRPC

###What is it?

It's a modern open source remote procedure call that runs in any environment.

Like in all RPC's the methods must exist client side and server-side. They are established via protobuffers - messages with name-value pairs called fields inside. Once compiled via the gRPC, they generate classes which implement the methods and attributes required to run the RPC. 
If we do everything correctly (place the methods in each respective machine), all we need to do is call the RPC via the client.

###Example .proto

```
service HelloService {
  rpc SayHello (HelloRequest) returns (HelloResponse);
}

message HelloRequest {
  string greeting = 1;
}

message HelloResponse {
  string reply = 1;
}

```
This will generate a class in the language we choose.

##GraphQL

###What is it?

It's a query language and server side run time for API's that prioritizes giving clients the data they request. It's designed to make API's fast and flexible

###GraphQL terms

**Schema** describes all the possible data clients can query. It's used to validate queries.

```
type Character {
  name: String!
  appearsIn: [Episode!]!
}

```

In this example, character is of Object Type. Meaning it has fields. The field name is of type String! and appearsIn is of type Episode! The brackets means its an array.

```
type Starship {
  id: ID!
  name: String!
  length(unit: LengthUnit = METER): Float
}

```
In this example we see the fields can have zero or more arguments. Field, in this case, unit has one argument: LengthUnit. Meter is default if it's not passed.

**Query** It's the default. Queries are composed by fields within fields.

###Example Query

```
query {
  repository(owner:"octocat", name:"Hello-World") {
    issues(last:20, states:CLOSED) {
      edges {
        node {
          title
          url
          labels(first:5) {
            edges {
              node {
                name
              }
            }
          }
        }
      }
    }
  }
}

```
In this query, we fetch repository from octocat with name Hello World, finds the 20 most recent closed issues and returns each issues title and url and the first 5 labels.

**Mutations**  Are used for modifications. They have a name, input object and payload object. The input object is composed of input fields, the data to be inserted is passed as the value of that input field. The payload object is the data I want to return from the server. It's composed of return fields. It's the body of the mutation name.

###Example Mutation

```
mutation AddReactionToIssue {
  addReaction(input:{subjectId:"MDU6SXNzdWUyMzEzOTE1NTE=",content:HOORAY}) {
    reaction {
      content
    }
    subject {
      id
    }
  }
}

```

**Variables** make queries more dynamic and powerfull. They are declared in the root of the query and passed within the operation.

###Example Query with variables

```
query($number_of_repos:Int!) {
  viewer {
    name
     repositories(last: $number_of_repos) {
       nodes {
         name
       }
     }
   }
}
variables {
   "number_of_repos": 3
}

```

**Fragments** can be used to share logic being any declared Object.

###Example fragment schema

```

fragment NameParts on Person {
  firstName
  lastName
}

```

###Example query with usage of a fragment

```
query GetPerson {
  people(id: "7") {
    ...NameParts
    avatar(size: LARGE)
  }
}
```
**You precede an included fragment with three periods (...)**

**Directives** allows us to do conditional logic, that is, imagine a particular application has a admin or not admin status. If you are admin you see admin stuff, if you are not, you won't. Directives solve this.

###Example schema with directives

```
  hero(episode: $episode) {
    name
    friends @include(if: $withFriends) {
      name
    }
  }
}
```

###Example query with directives value set

```
{
  "episode": "JEDI",
  "withFriends": false
}
```
**Enum** allows us to validate enum values agains't schema values. Basically it makes sure that the values in the schema match the ones in the enum.

###Example enum schema

```
enum Episode {
  NEWHOPE
  EMPIRE
  JEDI
}

```

**Interface** basically ensures a type object implemented from another object will have the types from the other object.

###Interface Examples Schema

```
interface Character {
  id: ID!
  name: String!
  friends: [Character]
  appearsIn: [Episode]!
}

type Human implements Character {
  id: ID!
  name: String!
  friends: [Character]
  appearsIn: [Episode]!
  starships: [Starship]
  totalCredits: Int
}

type Droid implements Character {
  id: ID!
  name: String!
  friends: [Character]
  appearsIn: [Episode]!
  primaryFunction: String
}

```

**Unions** let us get only one type of the types selected.

###Example Union

`union SearchResult = Human | Droid | Starship`

```
 search(text: "an") {
    __typename
    ... on Human {
      name
      height
    }
    ... on Droid {
      name
      primaryFunction
    }
    ... on Starship {
      name
      length
    }
  }
}

```

##GraphQL Introspection

`fragment+FullType+on+__Type+{++kind++name++description++fields(includeDeprecated%3a+true)+{++++name++++description++++args+{++++++...InputValue++++}++++type+{++++++...TypeRef++++}++++isDeprecated++++deprecationReason++}++inputFields+{++++...InputValue++}++interfaces+{++++...TypeRef++}++enumValues(includeDeprecated%3a+true)+{++++name++++description++++isDeprecated++++deprecationReason++}++possibleTypes+{++++...TypeRef++}}fragment+InputValue+on+__InputValue+{++name++description++type+{++++...TypeRef++}++defaultValue}fragment+TypeRef+on+__Type+{++kind++name++ofType+{++++kind++++name++++ofType+{++++++kind++++++name++++++ofType+{++++++++kind++++++++name++++++++ofType+{++++++++++kind++++++++++name++++++++++ofType+{++++++++++++kind++++++++++++name++++++++++++ofType+{++++++++++++++kind++++++++++++++name++++++++++++++ofType+{++++++++++++++++kind++++++++++++++++name++++++++++++++}++++++++++++}++++++++++}++++++++}++++++}++++}++}}query+IntrospectionQuery+{++__schema+{++++queryType+{++++++name++++}++++mutationType+{++++++name++++}++++types+{++++++...FullType++++}++++directives+{++++++name++++++description++++++locations++++++args+{++++++++...InputValue++++++}++++}++}}` 

Basically tells the graphql to spit its schema.

##GraphQL cheatsheet

### Common Attacks

NoSQL, SQL, OS Command Injection, SSRF, CRLF

###Examples

```
{
  doctors(
    options: "{\"limit\": 1, \"patients.ssn\" :1}", 
    search: "{ \"patients.ssn\": { \"$regex\": \".*\"}, \"lastName\":\"Admin\" }")
    {
      firstName lastName id patients{ssn}
    }
}

{ 
    bacon(id: "1'") { 
        id, 
        type, 
        price
    }
}

```

DoS

Abuse of broken authorization, improper or excessive, IDOR.

Batching Attacks

Security Misconfigurations

###Good practices

1. Use a list of allowed characters.

2. Reject invalid input gracefully.

3. Define schemas for mutations input.

4. Choose libraries that prevent injection and utilize them correctly.

5. Add limiting to the query, depth, ammount, pagination, rate-limiting

6. Disable introspection

7. Don't return excessive errors.

