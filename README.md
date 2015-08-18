# PTOLEMY - THE NETWORK CARTOGRAPHER

This repository is under active development.  If you take a clone, you are getting the latest, and perhaps not entirely stable code.

## Table of Contents
* [ABOUT](#about)
* [INSTALLATION](#installation)


## ABOUT

_Ptolemy_ is a Python Library and Web Tool for [LLDP](https://en.wikipedia.org/wiki/Link_Layer_Discovery_Protocol) network visualization tool. This tool represents the LLDP networks in terms of bidirectional network graph diagrams showing various connections and interfaces between the devices and giving a high level overview of the network. Mapping an entire network topology into a diagram is a tedious task and might take hours and various licensed tools to be done manually. Editing these diagrams once the network topology changes gets even more tedious and time consuming foe very complex networks. We have tried to automate this process and provide customers with an ***open source*** and easy to use tool to map a topology within minutes and few simple steps.

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
	

## USAGE

***
NOTE : Devices which the script attempts to connect must have NETCONF and LLDP enabled on the specified port or the default port
***

### Web UI


### Python Script 



## KNOWN ISSUES
- No Support for Python 3
- Issues with graphviz-2.38 and 2.39

## COPYRIGHTS AND LICENSE

Copyright 2015 Juniper Networks, Inc. under the [Apache License](LICENSE)
  
## CONTRIBUTORS
	
  - [Rob Cameron](https://github.com/RobWC)
  - [Kurt Bales](https://github.com/kwbales)
  - [Animesh Kumar](https://github.com/animesh-kumar)

## THANKS

Developing this tool wouldn't have been possible without [Python](https://www.python.org), [Junos PyEz](https://github.com/Juniper/py-junos-eznc), [Graphviz](http://www.graphviz.org), [PyGraphviz](http://pygraphviz.github.io),[AngularJS](https://angularjs.org), [JQuery](https://jquery.com), [Angular-Xeditable](http://vitalets.github.io/angular-xeditable/) and [jQuery.panzoom](http://timmywil.github.io/jquery.panzoom/).


