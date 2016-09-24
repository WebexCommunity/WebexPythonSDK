# ciscosparkapi
Simple, lightweight and scalable Python API wrapper for the Cisco Spark APIs

## Overview
Provides single Pythonic wrapper class that represents the Cisco Spark API interfaces and returned JSON objects as native Python objects.

 * Supports Python versions 2 and 3.
 
 * Leverages generator containers and RFC5988 web linking to provide simple and efficient 'paging' of Cisco Spark data objects returned by the Cisco Spark cloud.

 * All Cisco Spark JSON objects and attributes are represented as native python objects.
   * As new Cisco Spark attributes are added and returned by the Spark cloud service, they will be automatically available in the respective Python objects - no library update required.
   * New object types can be quickly created and modeled by via the generic SparkData class, or you can easily subclass SparkData to provide additional functionality.

 * The CiscoSparkAPI class facilitates the creation of simple 'connection objects.'  All API calls are wrapped by this single class, and are available via a simple hierarchical structure - like CiscoSparkAPI.rooms.list().
   * Argument defaults are provided to make getting connected simple, and can be easily overridden if needed.
   * The only setting required to get connected is your Cisco Spark Access Token (see [developer.ciscospark.com](https://developer.ciscospark.com/getting-started.html)).  When creating a new CiscoSparkAPI object, you may provide your access token one of two ways:
     1. By setting a SPARK_ACCESS_TOKEN environment variable.
     2. Via the ```CiscoSparkAPI(access_token="")``` argument.
   * All API calls are provided as simple method calls on the API connection objects.


## Installation
ciscosparkapi is available on PyPI.  Install it via PIP, or alternatively you can download the package from GitHub and install it via setuptools.

**PIP Installation**
```
$ pip install ciscosparkapi
```

**git / setuptools Installation**
```
$ git clone https://github.com/CiscoDevNet/ciscosparkapi.git
$ python setup.py install
```

## Examples

```python
from ciscosparkapi import CiscoSparkAPI


# By default retrieves your access token from the SPARK_ACCESS_TOKEN environement variable
api = CiscoSparkAPI()


rooms = api.rooms.list()    # Returns an generator container providing support for RFC5988 paging
for room in rooms:          # Efficiently iterates through returned objects
    print room.title        # JSON objects are represented as native Python objects


# Creating a list from the returned generator containers is easy
teams = api.teams.list()
team_list = list(teams)
print teams_list
```


## Current Status
**Beta(s) Released!**

Please check the [releases page](https://github.com/CiscoDevNet/ciscosparkapi/releases) for details on the latest releases.

We have released the first beta distributions for this package!  Please test out the package for your use cases, and raise [issues](https://github.com/CiscoDevNet/ciscosparkapi/issues) for any problems you encounter.  Also, **PLEASE** create new [issues](https://github.com/CiscoDevNet/ciscosparkapi/issues) to provide any feedback on the package API structure (names, method calls and etc.).  The package APIs are still subject to change, and we would like to get these nailed down before we release v1 for the package.


## Community Development Project Information
This is a collaborative community development project working to create two packages to be published to the Python Package Index:

  1. [**ciscosparkapi**](https://github.com/CiscoDevNet/ciscosparkapi) - Simple, lightweight and scalable Python API wrapper for the Cisco Spark APIs
  2. [**ciscosparksdk**](https://github.com/CiscoDevNet/ciscosparksdk) - Additional features and functionality useful to developers building on Cisco Spark API

Contributions and feedback are welcome.  Information on contributing this project can be found [here in the project Charter](https://github.com/CiscoDevNet/spark-python-packages-team/blob/master/Charter.md).
