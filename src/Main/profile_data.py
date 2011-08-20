import re
from sys import exit
import os

#pprint is just to print out the list elements in each line for readablity while debugging
from pprint import pprint

def fetch_Profile_data(file_profile, file_name):
    """
    This module accepts html page and the name of the file to write the data into. It extracts the information given by the user. 
    Name and friends list available publicly
    
    """


    profile_data = []
    for line_profile in file_profile.readlines():

#        this is to match the name of the person and store it in name variable
        regex_for_name = re.compile(r""".*<meta property="og:title" content="(.*?") />""")    
        name_found = regex_for_name.match(line_profile)
    
        if name_found: 
            name = name_found.group(1)
            print "New file Created - " + file_name
            profile_data_file = open(file_name, 'w')
            
# To ignore the " in the name at the end, slice the name till last character i.e. ignore last character            
            profile_data_file.write(name[:-1])
            profile_data_file.write("\n")
            
        


        if re.match(r'.*<script>big_pipe.onPageletArrive\(\{"phase":5,"id":"pagelet_people_same_name".*',line_profile):
            

#            split the line into elements with href=\" as seperator of elements
#            if that element has first nine 9 characters has http:\/\/\
#            than take the characters of that element from 1st character upto the first character having " but not including the "
#            example value stored as elements in friends_link :
#            http://www.facebook.com/people/Janak-Bhosale/100000817564826
            same_name_link = [  line[ : line.find('"') ] for line in line_profile.split(r'href=\"') if line[:9] == 'http:\/\/']    
    
    
#            the list formed has same values twice, to remove those values twice we will take odd values from the list
#            hence the flag changing alternatively
#            also name has a " at the end, to skip it i am slicing it till the last character but not including it
            flag = True
                           
            for person in same_name_link:
                if flag:
                    flag = False
                    
#                    remove all the \\ found in the links
                    p = re.compile( r'\\')
                    person = p.sub('', person)
                    print "Added Same name person = " + person
                    profile_data.append(person)

                else:
                    flag = True
            
        
#        all friends links are in this pagelet_relationship line, with re match that particular line
        if re.match(r'.*<script>big_pipe.onPageletArrive\(\{"phase":5,"id":"pagelet_relationships".*',line_profile):
            

#            split the line into elements with href=\" as seperator of elements
#            if that element has first nine 9 characters has http:\/\/\
#            than take the characters of that element from 1st character upto the first character having " but not including the "
#            example value stored as elements in friends_link :
#            http://www.facebook.com/people/Janak-Bhosale/100000817564826
            friends_link = [  line[ : line.find('"') ] for line in line_profile.split(r'href=\"') if line[:9] == 'http:\/\/']    
    
    
#            the list formed has same values twice, to remove those values twice we will take odd values from the list
#            hence the flag changing alternatively
#            also name has a " at the end, to skip it i am slicing it till the last character but not including it
            flag = True
                           
            for friend in friends_link:
                if flag:
                    flag = False
                    
#                    remove all the \\ found in the links
                    p = re.compile( r'\\')
                    friend = p.sub('', friend)
                    
                    profile_data.append(friend)
                    profile_data_file.write(friend)
                    profile_data_file.write("\n")

                else:
                    flag = True
                    
#        Friend's data not available online
            
#    print out the final data - for debugging    
    
    
    if name:
#        print "----------New Data--------------"
#        pprint(profile_data)
        profile_data_file.close()

            
#        print "----------X----X----------"
        
        return profile_data
    
    else:
        print "Url has no data Name and Friends. Please Check URL"
        print "Exiting Program"
        exit(1)
        
        
#def addlink(line_profile, profile_data_file, write_to_file, ):
        
