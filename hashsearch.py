#!/usr/bin/env python3

# hashsearch.py is used to search the NSRL and VirusTotal for MD5 hash
# values.
# Copyright (C) 2016 Matthew Aubert
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# https://github.com/aubsec/hashsearch.git
# https://twitter.com/aubsec

#imports
import argparse
from argparse import RawTextHelpFormatter
import csv
import datetime
import hashlib
import os
import sys
import tempfile
import urllib.request
import zipfile

#Constants
API_KEY = 'd59a06e314884e3b55bb6710dfea3f21bb6e3b4eb58f42'

# Classes, modules, and functions start with Main() at the bottom.  Rest are in alphabetical order.
# Tree:
# class NSRL()
#   def CheckNSRLHash()
#   def GetNSRL()
# def ExceptionHandler()
# def Main()

class NSRL():

# CheckNSRLHash():
# Checks if the NSRL has already been downloaded.
# Then checks the SHA1 hash posted on the NSRL page to the hash of the existing NSRL.
# If file exists and hash matches, will return True.
# If file does not exist or the hash does not match, will return False.
    def CheckNSRLHash(self, ver):

# Setup local variables.
        webDoc = tempfile.gettempdir() + '/webDoc.htm'
        findString = 'SHA1(rds_' + ver.replace('.','') + 'u.zip'

# Cleans up variables removing newlines, returns, and periods where necessary.
        findString = findString.replace('\n','').replace('\r','')
        zipFile = os.getcwd() + '/rds_' + ver.replace('\n','').replace('\r','').replace('.','') + 'u.zip'

# Tries opening zipFie.
# If unsucessful, exception will return false to GetNSRL() and zip will be downloaded.
# If sucessful, will check the SHA1 hash of zipFile to the hash posted on webDoc. 
# If hashes match, will return True to GetNSRL().
        try:
            with open(zipFile, 'rb') as zipFileOpen:
                hashDigest = hashlib.sha1(zipFileOpen.read()).hexdigest()
                with open(webDoc, 'r') as webDocOpen:
                    for line in webDocOpen:
                        if findString in line:
                            checkHash = line[-41:]
                            checkHash = checkHash.replace('\n','').replace('\r','')

# If the hash from the nsrl page matches the hash of the zip file, then function returns True.
# If true is returned, program will not redownload the rds_<ver>u.zip file.
# If false is returned, GetNSRL() will download the rds_<ver>u.zip.
                            if checkHash == hashDigest:
                                sys.stderr.write('[+] NSRL already downloaded and matches hash of posted zip.\n[+] Skipping download.\n')
                                return True
                            else:
                                return False
        except:
            return False

# GetNSRL():
# Downloads and unzips the NSRL.
    def GetNSRL(self):

# Setup local variables.
        webDoc = tempfile.gettempdir() + '/webDoc.htm'
        urllib.request.urlretrieve('http://www.nsrl.nist.gov/Downloads.htm', webDoc)
        with open(webDoc, 'r') as webDocOpen:
            for line in webDocOpen:
                if '<p><h2>RDS' in line:
                    ver = str(line[16:20:] + '\n')
                    break
                else:
                    continue

# Create variable with name of zip file and cleaup newlines, returns, and periods.
        zipFile = os.getcwd() + '/rds_' + ver.replace('\n','').replace('\r','').replace('.','') + 'u.zip'

# Verifies whether the NSRL already exists in cwd.
# If it does, it checks the hash of the file.
        checkHash = self.CheckNSRLHash(ver)

# If the checkHash returns as False, the updated NSRL will be downloaded.
        if checkHash == False:
            sys.stderr.write('[+] Starting download of NSRL\n')
            url = 'http://www.nsrl.nist.gov/RDS/rds_' + ver + '/rds_' + ver.replace('.','') + 'u.zip'
            url = url.replace('\n', '').replace('\r', '')
            urllib.request.urlretrieve(url, zipFile)
            sys.stderr.write('[+] Download of NSRL was sucessful.\n')

# Unzips NSRLFile.txt from rds_<ver>.zip regardless of whether it is already there.
        with zipfile.ZipFile(zipFile) as zf:
            sys.stderr.write('[+] Unzipping NSRLFile.txt.\n')
            zf.extract('NSRLFile.txt', os.getcwd()) 

# Return to Main() once completed.
        return 0


# ExceptionHandler():
# Collects error codes and prints to screen
def ExceptionHandler(errorValue, function):
    sys.stderr.write('[!] An error has occured in function ' + function + '\n')
    sys.stderr.write('[!] ' + str(errorValue) + '\n')
    exit(1)

# Main():
# Function parses the arguments and sets them to variables.
# Instatintiates the first object and passes execution to the object nsrl.
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
    parser.add_argument('-a', '--api', help='Optional. Specify a VirusTotal API Key.  Can also modify the value of the API_KEY constant.', required=False)
    parser.add_argument('-m', '--md5', help='Optional. Specify a single MD5 hash value to search.', required=False)
    parser.add_argument('-M', '--MD5-List', help='Optional. Specify a text list of MD5 hash values to search.', required=False)
    args = parser.parse_args()

# These are here for debugging purposes.
    #sys.stderr.write(str(args.start) + '\n')
    #sys.stderr.write(str(args.end) + '\n')

# Executes primary purpose of application.
    try:
        nsrl = NSRL()
        nsrl.GetNSRL()
        sys.stderr.write('[+] Program completed sucessfully.\n')
        exit(0)

# If execution fails, collects errors and passes them to the ExeceptionHandler() function.
    except Exception as errorValue:
        function = 'Main()'
        ExceptionHandler(errorValue, function)

if __name__=='__main__':
    Main()
