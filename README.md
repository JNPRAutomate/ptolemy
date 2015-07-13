# ptolemy - The network cartographer

# Prerequisites
1) Make sure you have [Python installed](https://wiki.python.org/moin/BeginnersGuide/Download) on your machine (Preferred version is 2.7.x). <br/>
  Python 3 and above is not supported.<br/>
2) [Install Graphviz](http://www.graphviz.org/Download..php) (Preferred version is graphviz-2.38 since graphviz-2.39 has few bugs) and [Pygraphviz](http://pygraphviz.github.io/documentation/pygraphviz-1.3rc1/install.html) for graph diagrams.<br/>

# Usage

NOTE : Devices which the script attempts to connect must have NETCONF enabled on the specified port or the default port

```
python ptolemy.py -f <csv_file_path>

-f : indicates option to provide device information in the form of a CSV.
The program currently supports only device information in form of a CSV.
```

A valid CSV will have:-
1) Hostname<br/>
2) Username<br/>
3) Password or SSH Key Path or both<br/>
4) Port Number (optional)<br/>

Sample CSV

```
Hostname,Username,Password,SSH Key Path,Port
172.21.202.223,animesh,abc@123,,
172.21.202.39,animesh,,/home/vagrant/code/ptolemy/ssh/vagrant,830
172.21.202.36,animesh,abc@123,/home/vagrant/code/ptolemy/ssh/vagrant,830
```

# Known Issues
- No Support for Python 3
- Issues with graphviz-2.39
