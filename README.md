# ptolemy - The network cartographer

# Prerequisites
1) Make sure you have Python installed on your machine (Preferred version is 2.7.x). <br/>
  Python 3 and above is not supported.<br/>
   [How to Install](https://wiki.python.org/moin/BeginnersGuide/Download)<br/>
2) Install Graphviz (Preferred version is graphviz-2.36 since graphviz-2.39 has few bugs) and Pygraphviz for graph diagrams.<br/>
   [Graphviz Installation ](http://www.graphviz.org/Download..php) and [PyGraphviz Installation] (http://pygraphviz.github.io/documentation/pygraphviz-1.3rc1/install.html)<br/>

# Usage

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

# Issues
- No Support for Python 3
- Issues with graphviz-2.39
