# -----------------------------------------------------------------------------
# Copyright 2025 Patrick Näf (herzbube@herzbube.ch)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -----------------------------------------------------------------------------

# Python modules
# - requests
# - requests-oauthlib

import json
import requests
import base64
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

# Some flags that control which parts of the program are executed
enableDebugPrints = True
enableBarcodeApiRequest = True
enableTrackConsignmentsApiRequest = True

# Constants used by the Barcode API call
labelImageType = "JPG"
labelImageBaseFileName = "label"

# Constants used by the Track Consignments API call
useIdentCodeFromBarcodeAPI = True
defaultIdentCode = "990003550700000017"

# Read secrets from file and initialize variables
with open('secrets.json', 'r') as file:
    secretsData = json.load(file)

if enableDebugPrints:
    print("Secrets data")
    print(secretsData)

clientId = secretsData["clientId"]
clientSecret = secretsData["clientSecret"]
frankingLicense = secretsData["frankingLicense"]

# --------------------------------------------------------------------------------
# Part 1: Authentication API request
# --------------------------------------------------------------------------------

token_url = "https://api.post.ch/OAuth/token"
scopes = ["DCAPI_BARCODE_READ", "MYSB_MAILPIECE_TRACKING_B2B_READ"]

# BackendApplicationClient uses "grant_type=client_credentials"
client = BackendApplicationClient(client_id = clientId, scope = scopes)
oauth2Session = OAuth2Session(client = client)

# The request body that is sent looks like this (without client ID and client secret):
#   grant_type=client_credentials&scope=DCAPI_BARCODE_READ+MYSB_MAILPIECE_TRACKING_B2B_READ
# The "+" is actually a space character encoded to application/x-www-form-urlencoded. Scopes must be separated by space
# characters according the OAuth 2.0 RFC: https://datatracker.ietf.org/doc/html/rfc6749#section-3.3
tokenResponse = oauth2Session.fetch_token(token_url = token_url, client_id = clientId, client_secret = clientSecret)

if enableDebugPrints:
    print("OAuth2 token response")
    print(tokenResponse)

access_token = tokenResponse["access_token"]
authorizationHeaderName = "Authorization"
authorizationHeaderValue = "Bearer " + access_token

# --------------------------------------------------------------------------------
# Part 2: Barcode API request
# --------------------------------------------------------------------------------

if enableBarcodeApiRequest:
    barcodeApiUrl = "https://dcapi.apis.post.ch/barcode/v1/generateAddressLabel"
    barcodeApiHeaders = {authorizationHeaderName: authorizationHeaderValue}

    # itemNumber notes:
    # - The itemNumber is used to construct the identCode that results from the Barcode API request.
    #   Example identCode from the documentation: 993590003400000002
    #                                                       ^^^^^^^^
    #                                                       The last 8 characters are the itemNumber
    # - If the Barcode API request contains an explicit itemNumber value, that value is used.
    # - If the Barcode API request does not contain an explicit itemNumber value, the Barcode API
    #   generates an itemNumber value by itself. Experimentally determined: The Barcode API starts
    #   with itemNumber 1, then continues by adding +1 to the lowest previously used itemNumber.
    #   Values that were used explicitly in Barcode API requests are skipped over.
    # - A previously used itemNumber may not be used again. If it is used again the Barcode API will
    #   respond with error E2016. The German error message uses the term "Sendungsnummer".
    # - Since the itemNumber range is limited to 8 digits, it is reasonable to assume that a previously
    #   used itemNumber will eventually become usable again. If this were not the case the Barcode API
    #   would become unusable once the number range has been exhausted. It is currently not known when
    #   or how a previously used itemNumber becomes usable again.
    #
    # Used itemNumbers so far:
    # - 1 - 21
    # - 666665 - 666668
    barcodeApiPayload = \
        {
            "language": "DE",
            "frankingLicense": frankingLicense,
            "customerSystem": "55",
            "customer": {
                "name1": "Test Kunde",
                "street": "Wankdorfallee 4",
                "zip": "3030",
                "city": "Bern",
                "domicilePostOffice": "3011 Bern",
                "country": "CH"
            },
            "labelDefinition": {
                "labelLayout": "A5",
                "printAddresses": "RECIPIENT_AND_CUSTOMER",
                "imageFileType": labelImageType,
                "imageResolution": 300
            },
            "sendingID": "777777",
            "item": {
                "itemID": "4444444",
               # "itemNumber": "20",
                "recipient": {
                    "postIdent": "3333",
                    "name1": "Hans",
                    "name2": "Muster",
                    "street": "Wankdorfallee",
                    "houseNo": "4",
                    "zip": "3030",
                    "city": "Bern",
                    "country": "CH"
                },
                "attributes": {
                    "przl": [
                        "PRI",
                        "SA"
                    ],
                    "weight": 12345
                }
            }
        }

    barcodeApiResponse = requests.post(url=barcodeApiUrl,
                                       headers=barcodeApiHeaders,
                                       json=barcodeApiPayload)
    barcodeApiResponseJson = barcodeApiResponse.json()

    # The "item" property is missing in some error cases, notably if the franking license is invalid
    if "item" in barcodeApiResponseJson:
        item = barcodeApiResponseJson["item"]
        hasErrors = "errors" in item

        if not hasErrors:
            identCode = item["identCode"]
        else:
            identCode = None
        # Always present, even in case of error
        labelsBase64 = item["label"]

        if enableDebugPrints:
            print(barcodeApiResponse.status_code)
            # Temporarily replace the base64 encoded image byte streams - this just clutters the debug output
            if not hasErrors:
                item["label"] = ["dummy-label-base64"]
            print (barcodeApiResponseJson)
            # Restore the base64 encoded image byte stream
            if not hasErrors:
                item["label"] = labelsBase64

        if not hasErrors:
            # Since we can provide multiple items in the request, there can be multiple label images in the response
            for index, labelBase64 in enumerate(labelsBase64):
                labelBytes = base64.b64decode(labelBase64)
                labelImageFileName = labelImageBaseFileName + "-" + str(index + 1) + "." + labelImageType.lower()

                if enableDebugPrints:
                    print("Writing label to file " + labelImageFileName)

                with open(labelImageFileName, "wb") as labelFile:
                    labelFile.write(labelBytes)

    else:
        if enableDebugPrints:
            print(barcodeApiResponse.status_code)
            print (barcodeApiResponseJson)

# --------------------------------------------------------------------------------
# Part 3: Track Consignments API request
# --------------------------------------------------------------------------------

if enableTrackConsignmentsApiRequest:
    # If the Barcode API request was made then identCode is set with the identCode value that resulted from the
    # request
    if useIdentCodeFromBarcodeAPI:
        mailpieceId = identCode
    else:
        mailpieceId = defaultIdentCode

    if enableDebugPrints:
        print("mailpieceId = " + mailpieceId)

    trackConsignmentsApiUrl = "https://mysb.apis.post.ch/logistics/mailpiece/tracking/business/v1//mailpieces"
    trackConsignmentsApiHeaders = {authorizationHeaderName: authorizationHeaderValue}
    trackConsignmentsApiPayload = \
        {
            "ids": mailpieceId,
        }
    trackConsignmentsApiResponse = requests.post(url=trackConsignmentsApiUrl,
                                                 headers=trackConsignmentsApiHeaders,
                                                 json=trackConsignmentsApiPayload)
    trackConsignmentsApiResponseJson = trackConsignmentsApiResponse.json()

    print(trackConsignmentsApiResponseJson)