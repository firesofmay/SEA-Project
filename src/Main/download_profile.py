
import urllib2
import cookielib
from sys import exit
import os



#this code might have some redundant code 
def download_profile(profile_link):
    """
    this code simply retrieves the files for me.
    
    """
    try:
        
        CHandler = urllib2.HTTPCookieProcessor(cookielib.CookieJar())
        browser = urllib2.build_opener(CHandler)
        browser.addheaders = [('User-agent', 'InFB - ruel@ruel.me - http://ruel.me')]
        urllib2.install_opener(browser)
     
        print 'Initializing..'
        
    #   return the html file 
        return browser.open(profile_link)
    
    except ValueError:
        
        print "Incorrect Input value, Please Enter a facebook url page."
        print "Exiting Program"
        exit(1)
        
    except urllib2.URLError:
        print "Incorrect URL Type, Please Enter correct Value OR Please Check your Internet Connection."
        print "Exiting Program"
        exit(1)
        
        