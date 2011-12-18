#!/usr/bin/python

"""
This downloads rohit sir's all friends successfully in a file called list.txt
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

    target = raw_input("Enter the Target Url\nExample (http://www.facebook.com/profile.php?id=123445566) OR\nhttp://www.facebook.com/username)\n: ")
    user = raw_input("Your Facebook Login ID: ")
    
    passw = getpass.getpass()

    #saving the userid
    n = re.compile("www\.facebook.com\/profile\.php\?id\=(\d+)|www\.facebook.com\/([\w.]+)")
    m = n.findall(target)
    
    if m == []:
        print "URL Error, please check your url"
        exit(2)
    elif m[0][0]:
        target = m[0][0]
        print "Userid = " + target
    elif m[0][1]:
        target = m[0][1]
        print "Username = " + target
    else:
        print "URL Error, please check your url"
        exit(2)
 
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
    res = browser.open('https://graph.facebook.com/%s?access_token=%s' % (target,acct))
    fres = res.read()
    jdata = json.loads(fres)
  
    #print jdata
    #print "````````````````````"
    
    # Get the users profile id and his name
    pid = jdata['id']
    pname = jdata['name']        
    
    print "Main profiles id = " + pid
    print "Profile Name = " + pname
        
    
    
    res = browser.open('http://m.facebook.com/profile.php?id=%s&v=info&refid=17' % pid)
    data = res.read()
    
    reFriends = re.compile(r'All Friends\s\(([\d,]+)\)') # gives the exact count of friends
    friendscount = reFriends.findall(data)[0]
    #Incase friends value has a , example 1,163, make it 1163
    if friendscount[1] == ",":
        friendscount = friendscount[0] + friendscount[2:]
    
    #converting friendscount to integer, and incrementing it by 10 so if its 691 it becomes 701 so that upper
    #range hits the value to 700 and we get all 691 friends
    friendscount = int(friendscount)
    
    print "Number of Friends = " + str(friendscount)
    time.sleep(5)                      
    if friendscount % 10 != 0:
        friendscount += 10
    
    listtxt = open(pname + "-" + pid + ".txt", 'w')
    data_list = []        
    count = 0
    for val in range(0,friendscount,10):
        print "inside val for loop, val = " + str(val)

        res = browser.open('http://m.facebook.com/friends/?id=%s&f=%s&refid=5&access_token=%s' % (pid, val, acct) )
        f = res.readlines()
        
        for line in f:
            d = open("debug.html", "w")
            d.write(line)


        for line in f:
        
                m = re.search("Add Friend", line)
            
                if m:
                    nameit = re.compile(u'name="[^>_=]+"><span>([^>_=]+)</span>')
                    n = nameit.findall(line)
                    n.reverse()
                    
                    matchit = re.compile(r'<div class="c"><a href=".profile.php\?id=([\d]+)|<div class="c"><a href=".([^?]+)')
                    l = matchit.findall(line)
                    
                    for (a,b) in l:
                        name = n.pop()
                        
                        if a:
                            listtxt.write(name + " , " + a)
                            listtxt.write("\n")

                            print "Name = " + name + "\t\t and "  + "Userid = " + a
                            count += 1
                        else:
                            listtxt.write(name + " , " + b)
                            listtxt.write("\n")
                            print "Name = " + name + "\t\t and "  + "Userid = " + b
                            count += 1
                    
                    print "Count of Friends = " + str(count)
                    #time.sleep(5)                  
 
    print "Done All Friends"
    listtxt.close


if __name__ == '__main__':
    main()

