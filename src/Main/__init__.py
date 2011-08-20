
# Standard Module Imports
import sys
from pprint import pprint
import re
import os

# Project Imports
from profile_data import fetch_Profile_data
from download_profile import download_profile

# pass this value for testing purpose
# http://www.facebook.com/profile.php?id=100000275937818

# Command to check the unique links found
# mankaj #@ cat * | sort -u | grep "http" | wc

# Command to list out people who have friends 
# mankaj #@ ll | cut -d" " -f7,10 | grep "[0-9][0-9][0-9] "

 
def main():
      
# for easy input of first link, comment these line in case you are using input directly from the command line
    sys.argv = raw_input('Enter command line arguments: ').split()
# adding a 0th index so that sys.argv functionality behaves normally
    sys.argv.insert(0, "commands inserted via user input to the program for interactivity")
        
    
# Initialize the list with the url    
    temp_link_url = [sys.argv[1]]
    
    while temp_link_url:
    
# pop out one url from the list            
        fetch_link = temp_link_url.pop(0)
        print "New value = " + fetch_link + "\n"
    
        file_name = create_file_name_from(fetch_link)
        
           
# check if user data already exists, if it does, skip it...
        if os.path.exists(file_name) == False:
            profile_page = download_profile(fetch_link)
            
# fetches the facebook profile data available publicly
# and updates the templink url to fetch, from all the links found.
            temp_link_url += fetch_Profile_data(profile_page, file_name)
        
            print "\n*************** Updated List**************\n"
            pprint(temp_link_url)
            print "\n***************X***XXXX***X***************\n"
            
        else:
            print "@@@@ File already Exists = " + file_name
        
    
    
def create_file_name_from(fetch_link):
        
# to remove all "/" as filename cant have a /
    p = re.compile( r'/')
    
# adding data files into projects data directory 
    file_name = "./data/"
    
# subsituting front slash with an underscore character & appending name of the file to the data directory
    file_name += p.sub('_', fetch_link[23:])
    
# appending extension .fbd (facebook data) to each profile data text
    file_name += ".fbd"
        
    return file_name


if __name__ == '__main__':
    main()