# ptolemy - The network cartographer


#Usage

```
python ptolemy.py -f <csv_file_path>

-f : indicates option to provide device information in the form of a CSV.
The program currently supports only device information in form of a CSV.
```

A valid CSV will have:-
1) Hostname
2) Username
3) Password or SSH Key Path or both
4) Port Number (optional)

Sample CSV

```
Hostname,Username,Password,SSH Key Path,Port
172.21.202.223,animesh,abc@123,,
172.21.202.39,animesh,,/home/vagrant/code/ptolemy/ssh/vagrant,830
172.21.202.36,animesh,abc@123,/home/vagrant/code/ptolemy/ssh/vagrant,830
```
