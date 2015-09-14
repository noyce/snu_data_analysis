'''
Author:Aseem Pathak
B.Tech CSE 2nd year
github.com/noyce
'''

from robobrowser import RoboBrowser
from bs4 import BeautifulSoup
import sqlite3

browser = RoboBrowser()
browser.open('http://myaccount.snu.edu.in/login.php')


signin_form = browser.get_form(id="frmUserLogin")
signin_form        


# Filling the login form
signin_form['snuNetId'].value = 'ab123' #sample form data
signin_form['password'].value = 'password_goes_here'


# And submit
browser.submit_form(signin_form)

#all netids stored in an array (this array can be huuuge depending on the netids)
batch_2014_netids =['ab123','xy456','nm890']
#dates array add/remove the dates you want to analize
#for eg. currently array is initialized to calculate weekly usage
dates=['2015-08-05','2015-08-11','2015-08-12','2015-08-18','2015-08-19','2015-08-25','2015-08-26','2015-09-01','2015-09-02','2015-09-08']
#initializing the week array (python newbie here)
week=[0,0,0,0,0]
x=0
i=0
d=0
conn = sqlite3.connect('netUsage.db')
c = conn.cursor()



for x in range(0,477):
    browser.open('http://myaccount.snu.edu.in')
    data_form = browser.get_form(id="frmUsageDtls")
    data_form         

    # Fill it out
    i=0
    d=0
    j=0
    for d in range(0,5):
        browser.open('http://myaccount.snu.edu.in')
        data_form['userNetId'].value = batch_2014_netids[x]
        data_form['startDate'].value = dates[j]
        data_form['endDate'].value = dates[j+1]
        j=j+2

    # And submit
        browser.submit_form(data_form)
        html_doc =str(browser.parsed())
        soup= BeautifulSoup(html_doc,'html.parser') 
        str1=soup.text
        str2="Total in GB"
        str3="GB: 0"
        str4="GB: 0."
        str5=str1[str1.find(str2) + 17*2 +1 :str1.find(str2)+(17*3)+5]
        str7=str5.replace(":","   ")
        
        #all print statements can be removed without affecting the database output
        if str5.find(str3)>0 and \
           str5.find(str4)<0:
            print(batch_2014_netids[x])
            
           
        else:
            print(x)
            print(batch_2014_netids[x])
            print(str1[str1.find(str2) + 17*2 +1 :str1.find(str2)+(17*3)+5])
            print('    ')
            print(str7[13:].strip())
            week[i]= float(str7[13:].strip())
            i=i+1
            
    if str5.find(str3)>0 and \
       str5.find(str4)<0:
        print(x)
    else:
        c.execute("insert into test2 (netId,week1,week2,week3,week4,week5) values(?,?,?,?,?,?)", (batch_2014_netids[x],week[0],week[1],week[2],week[3],week[4]))        
    x=x+1

conn.commit()
conn.close()

