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
```
pymysql
beautifulsoup4==4.9.1
bs4==0.0.1
certifi==2020.4.5.2
chardet==3.0.4
DateTime==4.3
idna==2.9
numpy==1.18.5
pandas==1.0.4
python-dateutil==2.8.1
pytz==2020.1
regex==2020.6.8
requests==2.24.0
six==1.15.0
soupsieve==2.0.1
urllib3==1.25.9
wheel==0.24.0
zope.interface==5.1.0
```
# Authors 
- Ariela Strimling, arstrim97@gmail.com
- Areej Eweida, areejeweida@gmail.com

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
