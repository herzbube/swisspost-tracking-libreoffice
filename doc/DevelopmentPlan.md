Summary
-------
This document outlines the plan how to develop this extension from the ground up to a fully functional first version.

Iteration 1
-----------
Basic proof of concept Python program that performs Swiss Post REST API requests. The resulting Python program shall do the following:

- Authenticate and get token
  - Take sensitive information (credentials and franking license) from a local file not committed to Git
- Send request to the Barcode API to create a barcode using dummy data
- Base64 decode the image
- Use the identCode resulting from the Barcode API request to send the Track Consignment API request

Iteration 2
-----------
Improve the POC 1 program so that it uses generated classes that match the OpenAPI definition. The goal is to make the code easier to maintain in the next iterations.

Iteration 3
-----------
- Transform the program into a reusable Python module that takes parameters instead of using dummy data
- Invoke the module from outside, supplying the dummy data

Iteration 4
-----------
- Turn the code into a LibreOffice extension that runs when a button is clicked
- The extension shall place the results of the REST API requests into a fixed location in a spreadsheet
- Barcode API result data: identCode + barcode image
- Track Consignment API result data: To be defined

Iteration 5
-----------
- Make the LibreOffice extension take its parameter values from fixed locations in a spreadsheet document
- Move the dummy data into a spreadsheet document
- Track consignment API request takes the identCode from the spreadsheet

Iteration 6
-----------
- Split Authentication, Barcode generation and Track Consignment into separate parts
- Button 1: Authenticate
- Button 2: Authenticate + generate barcode
- Button 3: Authenticate + track consignment

Iteration 7
-----------
- Design a scheme how to configure the extension so it takes its parameter values not from a fixed location and writes its results not to a fixed location
- Sensitive information is still stored in a local file

Iteration 8
-----------
Design a scheme where to store sensitive information

Iteration 9
-----------
Clean up and polish