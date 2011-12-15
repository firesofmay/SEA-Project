#!/usr/bin/python

"""
This downloads rohits friends page list successfully and able to fetch only the first few friends
to see more i have to simulate scroll down movement
m.facebook has a link to click
trying for that in FB 3
"""
 
import sys
import re
import urllib
import urllib2
import cookielib
import csv
import json

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
 
    
    res = browser.open('http://www.facebook.com/srivastwa?sk=friends&access_token=%s' % acct)
    
    #final data list
    listtxt = open('list.txt', 'w')
    
    data_list = []    
    for line_profile in res.readlines():

        if re.match(r'.*<div class="fbProfileBrowser".*',line_profile):        
            
            list = line_profile.split('div class="fsl fwb fcb"')
            #print list
            for item in list:
                item = re.search("(?P<url>https?://[^\s]+)", item).group()
                data_list.append(item)
                listtxt.write(item)
                listtxt.write("\n")
    
    listtxt.close


"""
    jdata = json.loads(fres)
 
    # Initialize the CSV writer
    fbwriter = csv.writer(open('%s.csv' % user, 'ab'), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
 
    # God for each ID in the JSON response
    for acc in jdata['data']:
        fid = acc['id']
        fname = acc['name']
 
        # Go to ID's profile
        res = browser.open('http://m.facebook.com/profile.php?id=%s&v=info&refid=17' % fid)
        xma = re.search('mailto:(.*?)"', res.read())
        if xma:
 
            # Replace the html entity from the scraped information
            email = xma.group(1).replace('&#64;', '@')
 
            # In case there will be weird characters, repr() will help us.
            try:
                print fname, email
            except:
                print repr(fname), repr(email)
 
            # Write to CSV, again with repr() if something weird prints out.
            try:
                fbwriter.writerow([fname, email])
            except:
                fbwriter.writerow([repr(fname), repr(email)])
 """
def usage():
    '''
        Usage: infb.py user@domain.tld password
    '''
    print 'Usage: ' + sys.argv[0] + ' user@domain.tld password'
    sys.exit(1)
 
if __name__ == '__main__':
    main()

