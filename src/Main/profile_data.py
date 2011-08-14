'''
Created on Aug 14, 2011

@author: mankaj
'''

#!/usr/bin/python

import re
import pprint

def fetch_Profile_data(file_profile):


     
    for line_profile in file_profile.readlines():
        regex_for_name = re.compile(r""".*<meta property="og:title" content="(.*?") />""")    
        name_found = regex_for_name.match(line_profile)
    
        if name_found: 
            name = name_found.group(1)
    
    
        if re.match(r'.*<script>big_pipe.onPageletArrive\(\{"phase":5,"id":"pagelet_relationships".*',line_profile):
            friends_link = [  line[ 9 : line.find('"') ] for line in line_profile.split(r'href=\"') if line[:9] == 'http:\/\/']    
    
            flag = True
            profile_data = []
            profile_data.append(name[:-1])
                           
            for friend in friends_link:
                if flag:
                    flag = False
                    p = re.compile( r'\\')
                    friend = p.sub('', friend)
                    profile_data.append(friend)
                else:
                    flag = True
                        
    pprint.pprint(profile_data)    

