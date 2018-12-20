# AIS and ASTERIX Python Decoder

This project was spawned based on a requirement to quickly and easily decode AIS and Cat10 messages. There was already a previous method to do this using two programs and some excel rework, but this took too long; especially for 
large datasets. Currently the decoder only works on Cat 10 messages and a subset of the total list of fields. This can be expanded if required.

The program utilizes a python library called simpleais and an asterix decoder (same one used by wireshark). 

## Getting Started

Run the decode.py script from your command line. Currently only tested with Windows 10.

### Prerequisites

- Python 3.x - https://www.python.org/
- Python simpleais library


### Installing

Download the folder from my public folder (where this README is located).


To run:

- open up Command Prompt
- Change directory to the AIS and ASTERIX Cat 10 folder
- run help script using python decode.py -h
- If no flags are used, default file names of AIS.csv and Cat10TrackData.pcap will be used.


## Authors

* **James Cox** - *Initial revision*

