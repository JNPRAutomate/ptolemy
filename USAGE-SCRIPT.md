### Python Script

In Python, you can run the application by just providing the script with a CSV file consisting of all the host names you want to connect to and their credentials.

***
Read the details about how a valid [CSV File](VALID-CSV.md) will look like.
***

The command should be of the following format :-

```
python ptolemy.py -i <csv_file_path>
```

The various parameter which are needed by the command are :-

* -i | --in : indicates option to provide device information in the form of a CSV. It's a mandatory argument.
The program currently supports only device information in form of a CSV.

Other optional parameters that can be specified are:-
* -u | --user : This parameter can be used for global authentication by specifying a global username which can be used by all hosts. This parameter must always be used  either with -p | --password or -s | --ssh option.
* -p | --password : Another parameter can be used for global authentication by specifying a global password which can be used by all hosts for specified global username.
* -p | --password : This parameter can be used for global authentication along with global username by specifying a global SSH Private Key File Path which can be used by all hosts.

A sample command to run the script with just an input CSV file will be as follows :-

```
python ptolemy.py -i csv/lldp.csv
```
A sample command to run the script with an input CSV file and global user credentials will be as follows :-

```
python ptolemy.py -i csv/lldp.csv --user = "animesh" --password="abc@123"

```
