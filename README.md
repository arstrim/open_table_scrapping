![image](https://logodix.com/logo/44715.png)

# OpenTable Scarper
This project will scrape, clean, and analyze 100 best restaurants in America for 2017.

## Overview 

- The data is retrieved and parsed from OpenTable web (main URL: https://www.opentable.com/m/best-restaurants-in-america-for-2017/) via a Beautiful Soup and Requests packages.
- Data is then cleaned and built in Python.
- Data is written to a MySQL database via PyMySQL connection.
- The data is deployed on an EC2 instance in AWS.
- Finally, the data is placed in ReDash for BI Analysis.

#  Project Status
- [![Build Status](http://img.shields.io/travis/sosedoff/opentable.svg?style=flat)](https://travis-ci.org/sosedoff/opentable)


# Flowchart
![alt text](https://github.com/areejeweida/opentable/blob/master/Capture.PNG?raw=true)

## Requirements
## Installation
[This file](https://github.com/arstrim/project/blob/master/requirements.txt) should be downloaded to later install it like:
```
pip install -r requirements.txt
```

# Authors 
- Ariela Strimling, arstrim97@gmail.com
- Areej Eweida, areejeweida@gmail.com

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
