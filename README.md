# ciscosparkapi
Simple, lightweight and scalable Python API wrapper for the Cisco Spark APIs

## Overview
A single Pythonic wrapper class representing the Cisco Spark API interfaces and returned JSON objects as method calls that return native Python objects.

 * Leverages generator containers and RFC5988 web linking to provide simple and efficient 'paging' of Cisco Spark data objects returned by the Cisco Spark clout.

 * All Cisco Spark JSON objects and attributes are represented as native python objects.
   * As new Cisco Spark attributes are added and returned by the Spark cloud service, they will be automatically available in the respective Python objects - no library update required.
   * New object types can be quickly created and modeled by via the generic SparkData class, or you can easily subclass SparkData to provide additional functionality.

 * The CiscoSparkAPI class facilitates the creation of simple 'connection objects' that are associated with the access_token used to create the object.  All API calls are wrapped by this single class, and are available via a simple hierarchical structure - like api.rooms.list().
   * API defaults are provided to make getting connected simple, and can be easily overridden if needed.
   * The only setting required to get connected is your Cisco Spark Access Token (see [developer.ciscospark.com](https://developer.ciscospark.com/getting-started.html)).
   * All API calls are provided as simple method calls on the API connection objects.

### Examples

```python
import os
from ciscosparkapi import CiscoSparkAPI


access_token = os.environ['SPARK_ACCESS_TOKEN']
api = CiscoSparkAPI(access_token, timeout=60)


rooms = api.rooms.list()    # Returns an generator container providing support for RFC5988 paging
for room in rooms:          # Efficiently iterates through returned objects
    print room.title        # JSON objects are represented as native Python objects


# Creating a list from the returned generator containers is easy
team_list = list(api.teams.list())
print team_list
```


## Community Development Project Information
This is a collaborative community development project to create two packages to be published to the Python Package Index:

  1. [**ciscosparkapi**](https://github.com/CiscoDevNet/ciscosparkapi) - A simple, scalable and lightweight API wrapper for the Cisco Spark services APIs
  2. [**ciscosparksdk**](https://github.com/CiscoDevNet/ciscosparksdk) - Additional features and functionality useful to Cisco Spark API developers

All are welcome to contribute to this project.  Information on contributing this project can be found [here in the project Charter](https://github.com/CiscoDevNet/spark-python-packages-team/blob/master/Charter.md).

## Current Status
**Wrappers for all Cisco API endpoints and data objects have now been completed!**


_Beta release imminent._
We are preparing to release the first _beta_ for this package.  Please test out the package for your use cases, and raise issues for any problems you encounter.  Also, **PLEASE** create new issues to provide feedback and foster discussion on the package API structure (names, method calls and etc.).  The package APIs are still subject to change, and I would like to get these nailed down before we release v1 for the package.
