# Project 3 - Distance Vector Algorithm

## To Run:
cd into tjd66-proj-3

Initialize Server First.

### Server
Example using proj3examplecsv-3.csv as config file 
```
python server.py proj3examplecsv-3.csv
```

### Client(s)
Example using node value 'u'
```
python client.py u
```

Client node value must be in the config file passed through the server. Otherwise, Client will be inactive in DV algorithm.

### Creating a Config File to match Server.py Load Process
Convert whatever format Config File you have into a python DataFrame.

Use df.to_csv(FILEPATH,index = None)

The csv file result will now be in the correct file format for server to process.
*  See proj3examplecsv-3.csv as file format example

