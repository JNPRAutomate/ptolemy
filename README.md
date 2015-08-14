# Ptolemy - The network cartographer

The repository is under active development.  If you take a clone, you are getting the latest, and perhaps not entirely stable code.



## DOCUMENTATION



## ABOUT

_Ptolemy_ is a Python Library and Web Tool for [LLDP](https://en.wikipedia.org/wiki/Link_Layer_Discovery_Protocol) network visualization tool. This tool represents the LLDP networks in terms of bidirectional network graph diagrams showing various connections and interfaces between the devices and giving a high level overview of the network. Mapping an entire network topology into a diagram is a tedious task and might take hours and various licensed tools to be done manually. Editing these diagrams once the network topology changes gets even more tedious and time consuming foe very complex networks. We have tried to automate this process and provide customers with an ***open source*** and easy to use tool to map a topology within minutes and few simple steps. The user is ***NOT*** required: (a) to be a "Software Programmer™", (b) have sophisticated knowledge of Junos, or (b) have a complex understanding of the Junos XML API.  

This library was built for two types of users:

### Easy to Use Web Tool


### Open and Extensible Python Script


## INSTALLATION

### Prerequisites
1) Make sure you have [Python installed](https://wiki.python.org/moin/BeginnersGuide/Download) on your machine (Preferred version is 2.7.x). <br/>
  Python 3 and above is not supported.<br/>
2) [Install PyEz](https://techwiki.juniper.net/Automation_Scripting/010_Getting_Started_and_Reference/Junos_PyEZ/Installation)	
3) [Install Graphviz](http://www.graphviz.org/Download..php) (Preferred version is graphviz-2.36 since graphviz-2.38 and 2.39 has few bugs) and [Pygraphviz](http://pygraphviz.github.io/documentation/pygraphviz-1.3rc1/install.html) for graph diagrams.<br/>

### Setting up Ptolemy

```
git clone https://github.com/JNPRAutomate/ptolemy.git
```
	

## Usage

NOTE : Devices which the script attempts to connect must have NETCONF and LLDP enabled on the specified port or the default port

```
python ptolemy.py -i <csv_file_path>

-i | --in : indicates option to provide device information in the form of a CSV. It's a mandatory argument.
The program currently supports only device information in form of a CSV.

Other optional parameters that can be specified are:-
-u | --user : This parameter can be used for global authentication by specifying a global username which can be used by all hosts. This parameter must always be used  either with -p | --password or -s | --ssh option.
-p | --password : Another parameter can be used for global authentication by specifying a global password which can be used by all hosts for specified global username.
-p | --password : This parameter can be used for global authentication along with global username by specifying a global SSH Private Key File Path which can be used by all hosts.

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

## Known Issues
- No Support for Python 3
- Issues with graphviz-2.38 and 2.39

## Copyrights and License

Copyright 2015 Juniper Networks, Inc. under the [Apache License](LICENSE)
  
## CONTRIBUTORS
	
  - [Rob Cameron](https://github.com/RobWC)
  - [Animesh Kumar](https://github.com/animesh-kumar)


