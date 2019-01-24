[![CircleCI](https://circleci.com/gh/brianhhq/aws-s3-storage-analysis-tool.svg?style=svg&circle-token=95d2fd54546d57ebe884b6ea33d169ced7bd8aec)](https://circleci.com/gh/brianhhq/aws-s3-storage-analysis-tool)
#  AWS S3 Storage Analysis Tool

A generic tool to get a quick view of AWS S3 Storage Inventory, Size, usage and Cost.


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 


### Prerequisites

What things you need to install the software and how to install them.
* Download and install [Docker](https://www.docker.com/get-started)
* To test the tool, you will have to create a [free Amazon account](https://aws.amazon.com/free/) (if you don't already have
one).


### Installing

Download the images via command line

```bash
docker login
docker pull brianhhq/aws-s3-storage-analysis-tool
```

### Usage

* Run the Container
```bash
docker run -d -t --name aws-s3-storage-analysis-tool brianhhq/aws-s3-storage-analysis-tool sh
```

* Run the tool
```bash
docker exec -e AWS_ACCESS_KEY_ID=<put your aws access id> -e AWS_SECRET_ACCESS_KEY=<put your aws access key> -t aws-s3-storage-analysis-tool python main.py
```


## Local Development

* Clone this project

* How to Build image
```bash
docker build -t <docker_username>/aws-s3-storage-analysis-tool .
```

* Run the Container `See Above`

* Enter the Container
```bash
docker exec -it aws-s3-storage-analysis-tool sh
```

* Stop and Clean up
```bash
docker stop aws-s3-storage-analysis-tool && docker rm aws-s3-storage-analysis-tool
```


* Run the program
```bash
python main.py
```

* Debug the program
```bash
DEBUG=true python main.py
```


## Running the tests

```bash
docker exec -e AWS_ACCESS_KEY_ID=<put your aws access id> -e AWS_SECRET_ACCESS_KEY=<put your aws access key> -t aws-s3-storage-analysis-tool python -m unittest tests.S3StatisticsTestCase
```

or

```
python -m unittest tests.S3StatisticsTestCase
```

## Built With

* [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) - Boto is the Amazon Web Services (AWS) SDK for Python, which allows Python developers to write software that makes use of Amazon services like S3 and EC2. Boto provides an easy to use, object-oriented API as well as low-level direct service access.


## Contributing

Please submit pull requests to us.


## Authors

* **Brian Huang**
* brian_hhq@hotmail.com


## License

This project is licensed under the MIT License.


### Highlight of the project

* [CI] Continuous Integration has been applied in this repo. CircleCI is chosen to be the CI tools to make sure building stuff faster, never shipping broken code and decreasing code review time.
* [Process Improvement]  Build caching mechanism has been considered to reduce the amount of building time.
* [Dockerization] Docker is chosen as a artifact as it increases CI Efficiency, simplifying configurations and ensures rapid deployment. It is also good to ship product across platform easily. 
* [Performance] The principle of minimum packages/images has been considered to ensure shipping smallest but functional application over low-bandwidth connection network.
* [Documentation] Documentation has been provided to make it easy for a user to run this program. Github integrates with CircleCI to quickly check the status of build status.
* [Code Style] Good practise of programming has been applied as I followed PEP 8 style guide. Comments have been applied where necessary. Right name conventions for functions, filename and variables have been considered for easy understanding. Logging mechanism is in place.
* [Unit Testing] Unit testing has been applied to ensure quality of code and find bugs earlier and easier.
* [Security] Branch protection rule(Signed Commit) has been applied. Commits pushed to matching branches must have [verified signatures](https://help.github.com/articles/signing-commits-using-gpg/) to ensure no one can pretend someone to commit. This is very important to large organisations with a lot of engineers. 
* [LOGGING] Logging feature has been implemented for the ease of trouble shooting. 