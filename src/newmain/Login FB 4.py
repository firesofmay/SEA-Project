#!/usr/bin/python

"""
This downloads rohit sir's all friends successfully in a file called list.txt
it automatically gets the count of friends, and also writes the name of friends to the list.txt
"""
 
import sys
import re
import urllib
import urllib2
import cookielib
import csv
import json
import time
import getpass

#pprint is just to print out the list elements in each line for readablity while debugging
from pprint import pprint
 
def main():

    user = raw_input("Login ID: ")
    passw = getpass.getpass()
 
    # Initialize the needed modules
    CHandler = urllib2.HTTPCookieProcessor(cookielib.CookieJar())
    browser = urllib2.build_opener(CHandler)
    browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686 on x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1')]
    urllib2.install_opener(browser)
 
    # Initialize the cookies and get the post_form_data
    print 'Initializing..'
    res = browser.open('http://m.facebook.com/index.php')
    mxt = re.search('name="post_form_id" value="(\w+)"', res.read())
    pfi = mxt.group(1)
    print 'Using PFI: %s' % pfi
    res.close()
 
    # Initialize the POST data
    data = urllib.urlencode({
        'lsd'               : '',
        'post_form_id'      : pfi,
        'charset_test'      : urllib.unquote_plus('%E2%82%AC%2C%C2%B4%2C%E2%82%AC%2C%C2%B4%2C%E6%B0%B4%2C%D0%94%2C%D0%84'),
        'email'             : user,
        'pass'              : passw,
        'login'             : 'Log+In'
    })
 
    # Login to Facebook
    print 'Logging in to account ' + user
    res = browser.open('https://www.facebook.com/login.php?m=m&refsrc=http%3A%2F%2Fm.facebook.com%2Findex.php&refid=8', data)
    rcode = res.code
    if not re.search('Logout', res.read()):
        print 'Login Failed'
 
        # For Debugging (when failed login)
        fh = open('debug.html', 'w')
        fh.write(res.read())
        fh.close
 
        # Exit the execution :(
        exit(2)
    res.close()
 
    # Get Access Token
    res = browser.open('http://developers.facebook.com/docs/reference/api')
    conft = res.read()
    mat = re.search('access_token=(.*?)"', conft)
    acct = mat.group(1)
    print 'Using access token: %s' % acct
 
    
#    res = browser.open('http://m.facebook.com/srivastwa?&access_token=%s' % acct)
    
    # Get friend's ID
    res = browser.open('https://graph.facebook.com/srivastwa?access_token=%s' % acct)
    fres = res.read()
    jdata = json.loads(fres)
  
    #print jdata
    #print "````````````````````"
    
    # Get the users profile id and his name
    pid = jdata['id']
    pname = jdata['name']        
    
    print "Main profiles id = " + pid
    print "Profile Name = " + pname
    
    res = browser.open('https://m.facebook.com/srivastwa')
    data = res.read()
    reFriends = re.compile(r'All Friends\s\((\d+)\)') # gives the exact count of friends
    friendscount = reFriends.findall(data)[0]
    
    #converting friendscount to integer, and incrementing it by 10 so if its 691 it becomes 701 so that upper
    #range hits the value to 700 and we get all 691 friends
    friendscount = int(friendscount)
    
    print "Number of Friends = " + str(friendscount)
    
    if friendscount % 10 != 0:
        friendscount += 10
    
    listtxt = open('list.txt', 'w')
    data_list = []        
    
    for val in range(0,friendscount,10):
        print "inside val for loop, val = %s" + str(val)

        res = browser.open('http://m.facebook.com/friends/?id=%s&f=%s&refid=5&access_token=%s' % (pid, val, acct) )
        
        #time.sleep(5)                  
        #final data list
        for line in res.readlines():
                print "inside line for loop"

                m = re.search("Add Friend", line)
            
                if m:
                    print "m found"
                    nameit = re.compile(u'name="[^>_=]+"><span>([^>_=]+)</span>')
                    n = nameit.findall(line)
                    print n
                    n.reverse()
                    
                    matchit = re.compile(r'<div class="c"><a href=".profile.php\?id=([\d]+)|<div class="c"><a href=".([^?]+)')
                    l = matchit.findall(line)
                    print l
                    for (a,b) in l:
                        name = n.pop()
                        
                        if a:
                            listtxt.write(a + "," + name)
                            listtxt.write("\n")

                            print "Userid = " + a + " \t\t and Name = " + name
                        else:
                            listtxt.write(b + "," + name)
                            listtxt.write("\n")
                            print "Userid = " + b + " \t\t and Name = " + name
                            
 
    print "Done All Friends"
    listtxt.close


if __name__ == '__main__':
    main()

