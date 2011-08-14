'''
Created on Aug 14, 2011
@author: mankaj
'''
import urllib2
import cookielib


#this code simply retrieves the files for me.
#this code might have some redundant code 
def download_profile(profile_link):
    CHandler = urllib2.HTTPCookieProcessor(cookielib.CookieJar())
    browser = urllib2.build_opener(CHandler)
    browser.addheaders = [('User-agent', 'InFB - ruel@ruel.me - http://ruel.me')]
    urllib2.install_opener(browser)
 
    print 'Initializing..'
    
#   return the html file 
    return browser.open(profile_link)
    