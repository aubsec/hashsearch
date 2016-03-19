# hashsearch.py
###https://github.com/aubsec/hashsearch.git

The purpose of this Python application is to take a CSV or individual hash value
as input, perform a search against the NSRL and VirusTotal for the input, and output
to stdout in CSV format data about the hashes discovered. 

## Usage

hashsearch.py requries at least one argument of either the -m or -M..

|Argument   |Description|
|---        |---|
|-a, --api |Specify a VirusTotal API key.|
|-h, --help |show this help message and exit|
|-m, --md5 |Specify a single MD5 hash|
|-M, --MD5-List|Specify a text file with a list of MD5 hashes|


Examples

Example 1:  hashsearch.py -m 0d1ef429ed4a31753e5905e5356ba94d

Example 2:  hashsearch.py -M md5-file.txt

## ToDo
- [x] NSRL Download, Unzip, and Hashcheck
- [ ] User input of single MD5 Hash
- [ ] User input of MD5 hash list
- [ ] VirusTotal search using constant API key.
- [ ] VirusTotal search using user defined API key.
- [ ] CSV formatted output to stdout.
- [ ] Fully commented.
- [ ] Error handling.

## Credits

Matthew Aubert
- @aubsec
- aubsec@gmail.com
- github.com/aubsec

## License

hashsearch.py is a tool for doing automated seraches of MD5 hash values
from VirusTotal and the NSRL.

Copyright (C) 2016 Matthew Aubert

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see http://www.gnu.org/licenses/.
