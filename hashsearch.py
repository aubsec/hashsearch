#!/usr/bin/env python3

# hashsearch.py is used to search the NSRL for MD5 hash values.
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
# https://aubsec.github.io

# Imports
import argparse
from argparse import RawTextHelpFormatter
import datetime
import hashlib
import os
import sys
import tempfile
import urllib.request
import zipfile


# Classes, methods, and functions.
# Organized by hierarchically and alphabetically by class, method, and function. 
# Organizational Tree:
# class NsrlLookup()
#   def checkNsrlHash()
#   def getNsrl()
#   def nsrlSearch()
# def ExceptionCheck()
# def ExceptionHandler()
# def Main()


# class NsrlLookup():
# Contains three methods:
#   def checkNsrlHash()
#   def getNsrl()
#   def nsrlSearch()
# Downloads NSRL zip file, verifies hash, and unzips appropriate file.
# Parses NSRLFile.txt for user specified string. 
# Outputs NSRLFile.txt line where there is a match.
class NsrlLookup():


# method checkNSRLHash():
# Checks if the NSRL has already been downloaded.
# Then checks the SHA1 hash posted on the NSRL page to the hash of the existing NSRL.
# If file exists and hash matches, will return True.
# If file does not exist or the hash does not match, will return False.
    def checkNsrlHash(self, ver):

# Setup local variables.
        webDoc = tempfile.gettempdir() + '/webDoc.htm'
        findString = 'SHA1(rds_' + ver.replace('.','') + 'u.zip'

# Cleans up variables removing newlines, returns, and periods where necessary.
        findString = findString.replace('\n','').replace('\r','')
        zipFile = str(os.getcwd() + '/rds_' + ver.replace('\n','').replace('\r','').replace('.','') + 'u.zip')

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
        
        except Exception as exceptValue:
            exceptFunction = 'NsrlLookup.checkNsrlHash()'
            return exceptValue, exceptFunction
        
        except:
            return False


# method getNsrl():
# Downloads and unzips the NSRL.
    def getNsrl(self):
        try:
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
            zipFile = str(os.getcwd() + '/rds_' + ver.replace('\n','').replace('\r','').replace('.','') + 'u.zip')

# Verifies whether the NSRL already exists in cwd.
# If it does, it checks the hash of the file.
            checkHash = False
            
            try:            
                checkHash = self.checkNsrlHash(ver)
            except:
                pass
            
# If the checkHash returns as False, the updated NSRL will be downloaded.
            
            if checkHash != True:
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
            return None, None

        except Exception as exceptValue:
            exceptFunction = 'GetNsrl.getNsrl()'
            return exceptValue, exceptFunction


# method nsrlSearch()
# Takes a string as input, seaches NSRLFile.txt for strings. 
# Prints line in NSRLFile.txt if string is in line. 
    def nsrlSearch(self, string):
        exceptFunction = 'NsrlLookup.nsrlSearch()'
        try:
            with open('NSRLFile.txt','r') as openNsrl:
                for line in openNsrl:
                    if string.lower() in line.lower():
                        print(line.strip().replace('"',''))
                    else:
                        continue
            return None, None

        except Exception as exceptValue:
            exceptFunction = 'NsrlLookup.nsrlSearch()'
            return exceptValue, exceptFunction

        except:
            return None, exceptFunction

# Begin Main

# function ExceptionCheck()
# Quick reusable function to check for exceptions.
def ExceptionCheck(exceptValue, exceptFunction):
    
    if exceptValue != None:
        ExceptionHandler(exceptValue, exceptFunction)
    else:
        return


# function ExceptionHandler():
# Collects error codes and prints to screen
def ExceptionHandler(exceptValue, exceptFunction):
    sys.stderr.write('[!] An exception has occured in ' + str(exceptFunction) + '\n')
    sys.stderr.write('[!] ' + str(exceptValue) + '\n')
    exit(1)


# function Main():
# Function parses the arguments and sets them to variables.
# Instatintiates the first object and passes execution to the object nsrl.
# Catches exception return values and calls ExceptionCheck or ExceptionHandler.
def Main():
    parser = argparse.ArgumentParser(description='''
hashsearh.py takes as input a text file of hashes or strings,  or a single hash value or string
and performs a searh of the NSRL.  The purpose is to identify if the provided MD5 hashes are known, 
allowing the analyst to focus their investigation.  The application will output to the stdout all 
findings in CSV format.

Example 1:  hashsearch.py -s 0d1ef429ed4a31753e5905e5356ba94d
Example 2:  hashsearch.py -s kernel32.dll
Example 3:  hashsearch.py -s File-Of-Strings.txt

It may also be beneficial to redirect the stdout to to a csv file like in the example below.

Example 4:  hashsearch.py -s kernel32.dll > out.csv


https://github.com/aubsec/hashsearch.git
https://twitter.com/aubsec
https://aubsec.github.io''', formatter_class=RawTextHelpFormatter)


    parser.add_argument('-s', '--string', help='Required. Specify a single hash value, string, or file of strings to search.', required=True)

    args = parser.parse_args()

# These are here for debugging purposes.
    sys.stderr.write('[+] String being parsed: ' + str(args.string) + '\n')

# Sets default exception values.
    exceptFunction = 'Main()'
    exceptValue = None

# Executes primary purpose of application.
    try:
# Instantiates object based on class NSRLDownload() and calls method GetNSRL().
        nsrl = NsrlLookup()
        
        exceptValue,exceptFunction = nsrl.getNsrl()

# Checks if an exception was returned from nsrl.getNsrl().
        ExceptionCheck(exceptValue,exceptFunction)
        
        sys.stderr.write('[+] Parsing NSRLFile.txt.\n ')

# Verifies that the NSRLFile.txt was actually unzipped to the cwd. 
# Also prints first line in NSRLFile.txt.
        try:
            fileTest = open('NSRLFile.txt', 'r')
            print(fileTest.readline().strip().replace('"',''))
            fileTest.close()
        
        except Exception as exceptValue:
            ExceptionHandler(exceptValue, exceptFunction)
       
# Searches NSRL for specified string, even if string is a file in cwd. 
        exceptValue, exceptFunction = nsrl.nsrlSearch(args.string)

# Test if string is a file being opened.
# If file is sucessfully open, loop through file and search NSRL for each line.                
        try:
            closedFile = str(os.getcwd() + '/' + args.string)
            with open(closedFile, 'r') as openFile:
            #with codecs.open(closedFile, "r",encoding='utf-8', errors='ignore') as openFile: 
                for line in openFile:
                    try:
                        line = line.strip()
                        exceptValue, exceptFunction = nsrl.nsrlSearch(line)
                    except:
                        continue
        except:
            pass

# This ExceptionCheck call is commented out on purpose.
# Due to encoding issues, it was generating an exception though the program completes sucessfully.
        #ExceptionCheck(exceptValue, exceptFunction)

# If program completed sucessfully, write sucess message to stderr and exit with 0.
        sys.stderr.write('[+] Program completed sucessfully.\n')
        exit(0)

# If execution fails, collects errors and passes them to the ExeceptionHandler() function.
    except Exception as exceptValue:
        ExceptionHandler(exceptValue, exceptFunction)

if __name__=='__main__':
    Main()
