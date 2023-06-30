# Goatlin Notes

## M1

### Content Provider

A `Content Provider` provides data to android applications such as activities, services or receivers.

**Providers with weak permissions or** `exportable:true` **allows exfiltrating the data used by that content provider**

`exportable:true` **implies all apps can query the content provider**

### adb shell content commands

`adb shell content` has **three** commands: `insert, query, delete`

#### Usage 

Since exportable is true, we can simply query, insert or delete with adb: `adb shell content query --uri content://com.cx.goatlin.accounts/Accounts`; `adb shell content insert --uri content://com.cx.goatlin.accounts/Accounts  --bind username:s:kotlin --bind password:s:goat`

## M2

### Data

**Data** can be **stored** in an app with several ways depending on the kind of data stored, the usage of the data and if that data should be kept private or be shared.

**Data** in **Android** can be **stored in**:

**App-specific storage**: External or internal storage that stores files meant to be used by the **app only**

**Shared Storage**: directories with files mean't to be shared by multiple apps

**KeyStore**: stores cryptographic keys and other sensitive information.

**Data** can be stored in the following formats:

**SQLite Databases** the preferred way

**Shared Preferences**: Stores key-pair values in a dedicated directory inside internal storage.

It's very common to find api keys, passwords, PII information inside the shared preferences and databases.

In goatlin, the user credentials after registration are stored in clear-text inside the database, and fetched with the same format after login:

`adb exec-out run-as com.cx.vulnerablekotlinapp cat /data/data/com.cx.vulnerablekotlinapp/databases/data > /tmp/kotlin-goat.sqlite`

## M3

**Mobile applications** exchange data in a **client-server** fashion.

### Certificate Pinning

**Certificate pinning** associates a certificate with a given host. It's how collections of valid certificates are **bound to one host**. If another certificate is **not within that collection, it is refused**.

Lack of certificate pinning can lead to **MiTM**


## M4

**Insecure Authentication** is fairly common due to mobile devices input factor: 4-digit PINs examplify this.

### Important

When **authentication happens locally**, it can be bypasses via jailbroken devices or through run time manipulation of the binary.

In Goatlin, Insecure Authentication and Insecure data storage walk hand in hand:

### Example

`adb exec-out run-as com.cx.vulnerablekotlinapp cat /data/data/com.cx.vulnerablekotlinapp/databases/data > /tmp/kotlin-goat.sqlite`

## M5

### Important

Whenever a bad actor returns your **encrypted information** to its **original form**, your cryptography was **insufficient**.

## M6

### Authentication vs Authorization

**Authentication** identifies something

**Authorization** validates permissions of something

## M7

### Goal

The **goal** is to **execute** foreign code within the mobile code's address.

**Buffer Overflows** and **memory leaks** should be top priorities.

## M8

### What is

**Code tampering** is directly modifying source-code by changing API's called, modify data and resources, manipulate memory content...

### Important

**Applications** should be able to detect whether its own code was tampered with based on what it knows about it's own integrity.

## M9 

### What is

**Reverse Engineering** is one of the first steps in a mobile application assessment because it allows to understand the application's internals:

**How's it working?**

**What kind of communcations are established?**

**Which libraries are used?**

Decompiling tools such as apktool  and jadx are used for this.

## M10

**Extraneous functionality** are functions or secrets hidden inside the app, and they allow an attacker to perform unintended actions:


**Debug functions**

**API KEYS**

**Hidden backend endpoints**
