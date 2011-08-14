'''
Created on Aug 14, 2011

@author: mankaj
'''

#!/usr/bin/python

import re

#pprint is just to print out the list elements in each line for readablity while debugging
import pprint

def fetch_Profile_data(file_profile):


     
    for line_profile in file_profile.readlines():

#        this is to match the name of the person and store it in name variable
        regex_for_name = re.compile(r""".*<meta property="og:title" content="(.*?") />""")    
        name_found = regex_for_name.match(line_profile)
    
        if name_found: 
            name = name_found.group(1)
    
#        all friends links are in this pagelet_relationship line, with re match that particular line
        if re.match(r'.*<script>big_pipe.onPageletArrive\(\{"phase":5,"id":"pagelet_relationships".*',line_profile):
            
#            split the line into elements with href=\" as seperator of elements
#            if that element has first nine 9 characters has http:\/\/\
#            than take the characters of that element from 9th character upto the first character having " but not including the "
            friends_link = [  line[ 9 : line.find('"') ] for line in line_profile.split(r'href=\"') if line[:9] == 'http:\/\/']    
    
    
#            the list formed has same values twice, to remove those values twice we will take odd values from the list
#            hence the flag changing alternatively
#            also name has a " at the end, to skip it i am slicing it till the last character but not including it
            flag = True
            profile_data = []
            profile_data.append(name[:-1])
                           
            for friend in friends_link:
                if flag:
                    flag = False
                    
#                    remove all the \\ found in the links
                    p = re.compile( r'\\')
                    friend = p.sub('', friend)
                    
                    profile_data.append(friend)
                else:
                    flag = True
                    
#    print out the final data - for debugging    
    pprint.pprint(profile_data)    

