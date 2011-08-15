'''
Created on Aug 14, 2011

@author: mankaj
'''

import profile_data
import download_profile
import sys

#pass this value on command line for testing purpose
#http://www.facebook.com/profile.php?id=100000275937818

def main():
    
    print "hello"
    
#    for easy input of first link, comment this line incase you are using input directly from the command line
    sys.argv = raw_input('Enter command line arguments: ').split()
#    adding a 0th index so that sys.argv functionality behaves normally
    sys.argv.insert(0, "commands inserted via user input to the program for interactivity")
    print sys.argv
    
#    downloads the link given via command line
    link = download_profile.download_profile(sys.argv[1])
    
#    fetches the facebook profile data available publically
    profile_data.fetch_Profile_data(link)

if __name__ == '__main__':
    main()