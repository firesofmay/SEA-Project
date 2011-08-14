'''
Created on Aug 14, 2011

@author: mankaj
'''

import profile_data
import download_profile
import sys

#'http://www.facebook.com/profile.php?id=100000275937818'

def main():
    
    link = download_profile.download_profile(sys.argv[1])
    profile_data.fetch_Profile_data(link)

if __name__ == '__main__':
    main()