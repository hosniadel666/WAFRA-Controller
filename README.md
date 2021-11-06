![Raspberry Pi](https://img.shields.io/badge/-RaspberryPi-C51A4A?style=for-the-badge&logo=Raspberry-Pi) &nbsp;
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)  &nbsp; 
![Qt](https://img.shields.io/badge/Qt-%23217346.svg?style=for-the-badge&logo=Qt&logoColor=white) &nbsp;
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white) &nbsp; 
![MySql](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white) &nbsp;
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white) &nbsp; 
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white) &nbsp;

 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
[![Python 3.6](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/) &nbsp;&nbsp;&nbsp;&nbsp;
![GitHub contributors](https://img.shields.io/github/contributors/hosniadel666/cvs_internship) &nbsp;&nbsp;&nbsp;&nbsp;
![GitHub last commit](https://img.shields.io/github/last-commit/hosniadel666/cvs_internship) &nbsp;&nbsp;&nbsp;&nbsp;


<!--[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) -->


## Table of contents
* [General info](#general-info)
* [Setup](#setup)
* [Control Server](#control-server)
* [Technologies and Tools](#technologies-and-tools)
* [GUI Application](#gui-application)



## General info
<p>The main goal of WAFRA is to develop a smart sustainable aquaponic system, monitored and controlled through photovoltaic powered remote sensing. The system would contribute to socio-economic growth and create new jobs in remote areas through offering a complete system that starts with training trainers and/or individuals on system operation and proposing a cost benefit analysis to start the system.</p>
<p>Here in this repository we are developing:</p>

* On-line monitoring system for water quality and system efficiency by developing a web server and installing it on an embedded board which will provide a service to collect sensors data and perform control actions.
* GUI application which will be installed in HMI(Human Machine Interface) in ecah field location.



## Setup
- To install dependencies for this project, run this bash script on your Raspberry Pi:
```
$ ./setup.sh
```

## Control Server
Discription of control server

### System Architecture
 <br/>
<p align="center">
  <img src="./resources/our_system_interaction.png">
</p> 

### Technologies and tools 
- Programming language: Python
- Development board: Raspberry PI 
- Framworks and libraries: Flask, PyQt5, hashlib, threading
- Database: SQLite
- Operating System: Rasbian(Debian-based OS)
- Source Code Management: GIT  
- Other tools: Postman, SSH, Remote Desktop Connection

### Run 
To run this project, install it locally on Raspberry Pi:

```
$ flask run -h ip:port
```

<!-- <details>
    <summary>Technologies</summary>
    <p>Content </p>
</details> -->


## GUI Application
<p align="center">
  <img src="./resources/our_system_interaction.png">
</p> 


### System Architecture
Discription of system architecture

### Technologies 
Discription of technology used
* python version : 3.8
### Run 
To run this project, install it locally on Raspberry Pi:

	
