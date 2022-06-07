# Jaspr Integration Testing

## Dependencies

### Install Pipenv
To run the integration tests you'll need to have pipenv installed. 
Follow the instructions here for help with installation: https://pipenv.pypa.io/en/latest/#install-pipenv-today

### Install secrets files
Additionally, you will need to download the secrets files from S3. 
They are located in Jaspr's Development AWS account.
S3 URIs:
* s3://jaspr-testing-config/integration-testing/data/development.json
* s3://jaspr-testing-config/integration-testing/data/release.json
* s3://jaspr-testing-config/integration-testing/data/integration.json
* s3://jaspr-testing-config/integration-testing/data/production.json

Download all of those files and put them into the `/test/data` folder.

## Running the tests

Then to run the tests all you need to do is run the following from the commandline:
```
cd test
pipenv install # This will take a minute
pipenv shell
python main.py # This will run the tests
```

## CLI Options

You can pass four CLI options to main.py. 

### --environment

This flag is used to tell the tests what configuration data it should use to run the tests. 
Configuration data contains things like username and password to login.

Default value is `release`.

Allowed values: `release`, `production`, `development`, `integration`

### --browser

This flag is used to specify what browser you want the tests to run in.
Allowed values are:
* 1 = Firefox
* 2 = Chrome
* 3 = IE
* 4 = Safari

Default value is Chrome (2).

### --baseurl

This flag specifies what the protocol and domain for testing is. 
This allows us to easily run tests against our localhost or deployments on AWS.

Default value is "https://jaspr-test--release.app.jaspr-development.com".

### --module

This flag specifies what test cases you want to run. 
If you are working in a specific file, it can save you time to ignore tests that aren't actively changing.

Default value is "jaspr_integration_testing.test_userflows" to run all tests.

### Example Usage

To run just the technician tests:
```
python main.py --module jaspr_integration_testing.test_userflows.test_technician
```

To run the tests in Firefox:
```
python main.py --browser 1
```

to run the tests against localhost with port 8080 using the development configuration:
```
python main.py --baseurl http://localhost:8080 --environment development
```