# Stori code challenge

Code challenge lambda that processes information from a csv file from an S3 bucket, extracts averages and number
of transactions per month, as well as mailing this information

## Getting started

Make sure you have installed

- [Python 3.9+](https://www.python.org/downloads/)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-macos.html)

## Installation

Make sure you have your aws-cli configurated, you can check this by executing the next command

```sh
aws configure
```

Setup your workspace:

```sh
git clone https://github.com/samEscom/stori_challenge.git stori_challenge
cd stori_challenge
make install
```

For this challenge:
* I created a bucket in S3 called "resumes-challenge" and added the example file, called example.csv, as well as another file, example2.csv.

* A DynamoDB table called "summaries" was created, where the processed fields are inserted.

* Use the local aws configuration to be able to run locally using a local script called run_local.py

## Use local

una vez configurado el entorno de aws de manera local, 
se puede ejecutar usando el script run_local.py

```sh
python run_local.py
```

#### example:

<img width="818" alt="run_local" src="https://github.com/samEscom/stori_challenge/assets/11033993/16401ae4-0996-4cd1-99fb-0c17b549892d">

## Testing

To run your tests, execute:

```sh
make tests
```
You can change the scope of the tests you want to run with the variable `TEST`:

```sh
make tests TEST=tests/routes
```

To run one specific test function, run:
```sh
make tests TEST={test/file.py}::{specific_test}
```

The coverage achieved in this phase of the test is the following

<img width="806" alt="coverage" src="https://github.com/samEscom/stori_challenge/assets/11033993/aff5786e-2534-497a-8184-ea974de9c243">


## Use with postman


Use on the header  "content-type": "application/json"

and the body like this

```javascript
{
    "email": "sa5m.escom@gmail.com",
    "fileName": "example.csv" // example2.csv could be option on my S3 bucket
}
```

* If the parameters are invalid, a statusCode 500 will be returned.

<img width="701" alt="invalid_params" src="https://github.com/samEscom/stori_challenge/assets/11033993/f1ba45f5-fda2-4ef0-85bc-0088ba43c61b">

* Same if the email is wrong format

<img width="682" alt="invalid_email" src="https://github.com/samEscom/stori_challenge/assets/11033993/df9a5c1c-fd67-4f00-9e42-8cee6df83d29">



* Only can use POST method, and if use GET or other method a statusCode 501 
will be returned

<img width="701" alt="invalid_method" src="https://github.com/samEscom/stori_challenge/assets/11033993/3ef3ea73-4048-4fd6-8321-8a264ea3f331">

* Use x-api-key on header to can call lambda from postman, the value is send on email

<img width="684" alt="invalid_access" src="https://github.com/samEscom/stori_challenge/assets/11033993/aef3f9d7-c593-4005-9adf-fe104bb3dbe9">


* if all success returned a statusCode 200

<img width="696" alt="success" src="https://github.com/samEscom/stori_challenge/assets/11033993/5341b61c-b940-43db-9e9f-4852c8079a08">


## Validation and lint

To check your code against everything, run:


```sh
make lint
```

Some of the errors can be fixed automatically through:

```sh
make lint-fix
```

#### Contact

- Email: `sa5m.escom@gmail.com`


