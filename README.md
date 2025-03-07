This is a LibreOffice extension written in the Python programming language with the purpose to track Swiss Post shipments via the [Swiss Post REST API](https://developer.apis.post.ch/ui/home).

# User information

## Prerequisites

To use this extension you first need to have a billing relationship with Swiss Post. Follow [this link](https://www.post.ch/en/business-solutions/become-a-business-customer) to get started.

Once you have established a billing relationship, the next thing you need to do is to register with Swiss Post to use the "Track consignment" REST API. Follow [this link](https://developer.apis.post.ch/ui/apis/f7abf4c4-4a6e-49d4-abf4-c44a6e69d481) to get started.

Once you have registered you are ready to install the extension and configure it with the credentials you received during registration.

**Important:** The "Track consignment" API identifies so-called "mail pieces" via "mail piece id". This is an id provided by Swiss Post when you generate an address label via their Barcode API. So you cannot use the "Track consignment" API - or in other words: this LibreOffice extension - without also using the Barcode API. To register for the Barcode API, follow [this link](https://developer.apis.post.ch/ui/apis/5cff6ab7-8325-4a05-bf6a-b783256a0552). Note however that generating address labels is not something this LibreOffice extension does.

## Installation

TODO Write instructions how to install the extension. This may be as simple as "double-click the .oxt file".

## Configuration

TODO Write instructions how to configure the extension. At least the storage of any secrets needed to access the REST APIs (e.g. OAuth credentials, API key, ...) must be covered by this.

# How to use

TODO Write instructions how to use the extension. For instance, how to feed a shipment ID into the extension.

# Developer information

## Dependencies

TODO Write something about the dependencies this extension has to other software, notably which Python packages it needs.

## Packaging

TODO Write instructions how to build the .oxt file.

## More documentation

- [LibreOffice Development notes](doc/LibreOfficeDevelopment.md)
- [TODO list](doc/TODO.md)


# License

This LibreOffice extension is released under the [Apache License](http://www.apache.org/licenses/LICENSE-2.0) (2.0). Here's the [link to the license file](LICENSE).
