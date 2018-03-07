# HTTP List Universities
A Python script that creates a server to access a CSV file. You can add, remove and list the lines in the CSV file. It's implemented using Python and HTML with the purpose of using the HTTP functions, such as *GET* and *POST*.

### Running
Run the scrip using the Python 3.6:

```sh
$ python3.6 server.py
```

### Accessing
To access it, go to http://localhost:8000 on your browser, followed by:

**/list** : Lists all the universities in the CSV file.

**/new** : Adds a new university name.

**/delete** : Deletes a university name.
