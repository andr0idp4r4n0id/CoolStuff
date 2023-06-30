### Protocols

## HTTP/2

#HTTP/1 & HTTP/2 equivalents

```
POST /login HTTP/1.1\r\n
Host: psres.net\r\n
User-Agent: burp\r\n
Content-Length: 9\r\n
\r\n
x=123&y=4

:method	POST
:path	/login
:authority	psres.net
:scheme	https
user-agent	burp
x=123&y=4 

```

The first line in HTTP/1 is the verb, endpoint and HTTP version. In HTTP/2, these are all replaced by pseudo-headers.

HTTP/1 is a text protocol, HTTP/2 is a binary protocol.

HTTP/2 supports bidirectional sequence of text format frames. They are called streams. This basically means there is less latency as these streams can run concurrently. Only one TCP connection is utilized. It can send additional cacheable information to the client that isn't required but anticipated to be. It uses HPACK, a header compression algorithm which compresses each header's value before transfering that to the server. A previously transfered header value is then used to reconstruct the full headers.

#HPACK Functionality

It has:

1. static compression - Uses a predefined wordlist of 61 commonly used header fields

2. Dynamic dictionary - Headers found from previously connections.

3. Huffman Encoding - ASCII digits and lowercase letters are given shorter encodings. The shortest is 5 bits long

It will first check the static and then dynamic dictionary looking for matches, and if it finds them, it will simply reference the entry in the dictionary, usually takes one byte. Two will suffice.
For example:

```
:method GET

```
Will always be present in the static wordlist, and as such, will always be encoded in a single byte.

Headers that do not match will be added to the dynamic dictionary, because fields usually repeat themselves, and as such, can be encoded to a single byte after being added to the dynamic dictionary.

At the first request, everything not matched will be huffman encoded and added to dynamic wordlist.

After that, those that match either of the wordlists are encoded to a single or two bytes, the rest is huffman encoded. And the logic repeats itself.

#Differences in both.

                                     HTTP/1                    | 		HTTP/2

**Parsing** : **string based operations** | **Predefined offsets**

**Message Length** : **Content-Length, Transfer-Encoding** | **The body is composed of data frames, each with a length field.** 