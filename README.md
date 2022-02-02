# WIP

## Signal-CLI-REST-API Command Line Client

This is a command line wrapper for [pysignalclirestapi](https://github.com/bbernhard/pysignalclirestapi).

Basically it Stores your Server URL, Number and optinaly your https auth credantials in a json file and makes all public methods of pysignalclirestapi avaliabe to the consol.

### Install:

```
python3 -m venv singnal-rest-api-client
source ./singnal-rest-api-client/bin/activate
pip install -r ./requirements.txt
```

### Usage:

```
source ./singnal-rest-api-client/bin/activate
python ./singnal-cli-rest-api-client.py --help
python ./singnal-cli-rest-api-client.py api_info help
python ./singnal-cli-rest-api-client.py api_info
```

### TODO:
- Write startup script
