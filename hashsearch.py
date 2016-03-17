#!/usr/bin/env python3

#    hashsearch.py is used to search the NSRL and VirusTotal for MD5 hash
#    values.
#    Copyright (C) 2016 Matthew Aubert
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    https://github.com/aubsec/hashsearch.git
#    https://twitter.com/aubsec

#imports
import argparse
from argparse import RawTextHelpFormatter
import csv
import datetime
import sys
import tempfile
import urllib.request
import zipfile

#Constants
API_KEY = 'd59a06e314884e3b55bb6710dfea3f21bb6e3b4eb58f42'

#Downloads and unzips the NSRL 
#TD 1.  Verify the NSRL package does not change.
#TD 2.  Have the function check to see if hte NSRL is already downloaded.
#TD 3.  Call 
def getNSRL():
    try:
        tmpFile = tempfile.gettempdir() + '/nsrl.zip'
        

        
        if os.path.isfile(tmpFile) == True:
            #Check hash value of tmpFile to the SHA hash value on NSRL site.
            #If hash value is different, delete tmpFile and download.
        else:
            continue
        
        
        
        
        sys.stderr.write('[+] Starting download of NSRL')
        url = 'http://www.nsrl.nist.gov/RDS/rds_2.50/rds_250m.zip' #The version number does change.  Modify to parse version number before downloading
        response = urllib.request.urlretrieve(url, tmpFile)
        sys.stderr.write('[+] NSRL downloaded to ' + directory + '/\n[+] Beginning unzip to ' + tempfile.gettempdir() + '/')
        unzip(tmpFile, tempfile.gettempdir()) 
        sys.stderr.write('[+] Download of NSRL was sucessful.')
        return 0
    except Exception as errorValue:
        function = 'getNSRL()'
        exceptionHandler(errorValue, function)
        return 1


#ExceptionHandler() collects error codes and prints to screen
def ExceptionHandler(errorValue, function):
    sys.stderr.write('[!] An error has occured in function ' + function + '\n')
    sys.stderr.write('[!] ' + str(errorValue) + '\n')
    exit(1)

# Main
def Main():
    parser = argparse.ArgumentParser(description='''
hashsearh.py takes as input a text file of MD5 hashes or a single MD5 hash value and performs 
a searh of the NSRL and VirusTotal.  The purpose is to identify if the provided MD5 hashes
are known Malicious or Known benign, allowing the analyst to focus their investigation.  The
application will output to the std.out all findings in CSV format.

Example 1:  hashsearch.py -m 0d1ef429ed4a31753e5905e5356ba94d
Example 2:  hashsearch.py -M md5-file.txt

https://github.com/aubsec/hashsearch.git
https://twitter.com/aubsec''', formatter_class=RawTextHelpFormatter)
    parser.add_argument('-a', '--api', help='Optional. Specify a VirusTotal API Key.  Can also modify the value of the API_KEY variable', required=False)
    parser.add_argument('-m', '--md5', help='Optional. Specify a single MD5 hash value to search.', type=dateFormat, required=False)
    parser.add_argument('-M', '--MD5-List', help='Optional. Specify a text list of MD5 hash values to search.', type=dateFormat, required=False)
    args = parser.parse_args()
    #sys.stderr.write(str(args.start) + '\n')
    #sys.stderr.write(str(args.end) + '\n')
    
    try:
        csvSorter(args)
        sys.stderr.write('[+] Program completed sucessfully\n')
        exit(0)
    except Exception as errorValue:
        function = 'Main()'
        ExceptionHandler(errorValue, function)

if __name__=='__main__':
    Main()
