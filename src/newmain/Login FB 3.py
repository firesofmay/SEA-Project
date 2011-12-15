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

#pprint is just to print out the list elements in each line for readablity while debugging
from pprint import pprint
 
def main():
    # Check the arguments
    if len(sys.argv) != 3:
        usage()
    user = sys.argv[1]
    passw = sys.argv[2]
 
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
    
    listtxt = open('list.txt', 'w')
    data_list = []        
    
    for val in range(0,690,10):

        res = browser.open('http://m.facebook.com/friends/?id=%s&f=%s&refid=5&access_token=%s' % (pid, val, acct) )
        
        #time.sleep(5)                  
        #final data list
        

        for line_profile in res.readlines():
            print str(val) + "\n"
            
            try:
                if re.match(r'.*<div class="c">.*',line_profile):        
                    
                    list = line_profile.split('<div class="c"><a href=')
                    
                    #pprint (list)

                    for item in list[1:]:
                        #matching ids without username
                        m = re.findall(r"profile.php\?id=(.\d+)", item)

                        if m:
                            print m[0]
                            data_list.append(m[0])
                            listtxt.write(m[0])
                            listtxt.write("\n")

                        else:
                            #matching ids with username
                            n = re.findall(r"/([a-zA-Z0-9\.\_]+)\?", item)

                            if n: 
                                print n[0]
                                data_list.append(n[0])
                                listtxt.write(n[0])
                                listtxt.write("\n")

            except:
                print "!!!!!!!!Error at = " + str(val) + "\n"
                pass

    print "Done All Friends"
    listtxt.close


def usage():
    '''
        Usage: infb.py user@domain.tld password
    '''
    print 'Usage: ' + sys.argv[0] + ' user@domain.tld password'
    sys.exit(1)
 
if __name__ == '__main__':
    main()

