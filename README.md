# Ptolemy - The Network Cartographer

This repository is under active development.  If you take a clone, you are getting the latest, and perhaps not entirely stable code.

## Table of Contents
1. [About](#about)
2. [Demo](#demo)
   1. [Demo Video for Web UI in Action]()
   2. [Demo Video for Python Script in Action]()
3. [Installation](#installation)
   1. [Prerequisites](#prerequisites)
   2. [Setting up Ptolemy](#setting-up-ptolemy)
4. [Usage](#usage)
   1. [Web UI](#web-ui)
   2. [Python Script](#python-script)
5. [Known Issues](#known-issues)
6. [Copyrights and License](#copyrights-and-license)
7. [Contributors](#contributors)
8. [Thanks and Credits](#thanks-and-credits)

## About

_Ptolemy_ is a Python Library and Web Tool for [LLDP](https://en.wikipedia.org/wiki/Link_Layer_Discovery_Protocol) network visualization tool. This tool represents the LLDP networks in terms of bidirectional network graph diagrams showing various connections and interfaces between the devices and giving a high level overview of the network. Mapping an entire network topology into a diagram is a tedious task and might take hours and various licensed tools to be done manually. Editing these diagrams once the network topology changes gets even more tedious and time consuming foe very complex networks. We have tried to automate this process and provide customers with an ***open source*** and easy to use tool to map a topology within minutes and few simple steps.

This library has two types of flavors:
 1. An Easy to Use Web Tool
 2. Open and Extensible Python Script

## Demo
1. [Demo Video for Web UI in Action]()
2. [Demo Video for Python Script in Action]()

## Installation

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

***
__NOTE__
 1. Devices which the script attempts to connect must have NETCONF and LLDP enabled on the specified port or the default port
 2. Web UI works best with Google Chrome Browser.
***

### Web UI

[Getting Started with Ptolemy using the Web UI](USAGE-WEB.md)


### Python Script 

[Getting Started with Ptolemy using the Python Scipt](USAGE-SCRIPT.md)


## Known Issues
- Web UI has Issues with Safari Browser - Works best with Google Chrome
- No Support for Python 3
- Issues with graphviz-2.38 and 2.39

## Copyrights and License

Copyright 2015 Juniper Networks, Inc. under the [Apache License](LICENSE)
  
## Contributors
	
  - [Rob Cameron](https://github.com/RobWC)
  - [Kurt Bales](https://github.com/kwbales)
  - [Animesh Kumar](https://github.com/animesh-kumar)

## Thanks and Credits

Developing this tool wouldn't have been possible without [Python](https://www.python.org), [Junos PyEz](https://github.com/Juniper/py-junos-eznc), [Graphviz](http://www.graphviz.org), [PyGraphviz](http://pygraphviz.github.io),[AngularJS](https://angularjs.org), [JQuery](https://jquery.com), [Angular-Xeditable](http://vitalets.github.io/angular-xeditable/) and [jQuery.panzoom](http://timmywil.github.io/jquery.panzoom/).


