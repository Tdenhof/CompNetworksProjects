# Project 3 - Distance Vector Algorithm
* In this project Node = routerID as it was easeier to write node instead of routerID everytime. Consider them the same.
## To Run:
cd into tjd66-proj-3

Initialize Server First.
Imports Used... Use Python Env that can handle these packages whether that be python3 or python. For my machine, I needed python3
'''
import pandas as pd
import sys
import util
import socket
import time
import ast
import pickle 
'''

### Server
Example using proj3examplecsv-3.csv as config file using python3 
```
python3 server.py proj3examplecsv-3.csv
```

### Client(s)
Example using node value 'u'
```
python3 client.py u
```
For example, to run the config file above I needed 7 total terminals open in VSCode...
1 for server, 1 for each (6) clients.


Client node value must be in the config file passed through the server. Otherwise, Client will be inactive in DV algorithm.

### Creating a Config File to match Server.py Load Process
Convert whatever format Config File you have into a python DataFrame.

Use df.to_csv(FILEPATH,index = None)

The csv file result will now be in the correct file format for server to process.
*  See proj3examplecsv-3.csv as file format example

