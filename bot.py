import pickle
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import schedule
class Meeting:
    def __init__(self,start_time,day_name,link,subject_name=None):
        self.link = link
        self.start_time = start_time
        self.day_name = day_name
        self.subject_name = subject_name

    def __str__(self):
        template = '''
        Time: {0}
        Day: {1}
        Link: {2}
        Subject name: {3}

        '''
        return template.format(self.start_time, self.day_name, self.link, self.subject_name)


class User:
    def __init__(self,email,password,browser, source):
        self.email = email
        self.password = password
        self.browser = browser
        self.source = source

    def __str__(self):
        template = '''
        Email: {0}
        Password: {1}
        Browser: {2}
        Source: {3}
        '''
        return template.format(self.email, self.password, self.browser, self.source)


def new_user():
    global user
    if user ==None:
        email = input("Write your email adres : ")
        password = input ("Write your password : ")
        browser = input ("Write your browser (chrome or edge) : ")
        browser = browser.lower()
        source = input ("Write your source : ")
        if browser=="chrome" or browser=="edge":
            user = User(email,password,browser,source)
        else:
            print("Uncorrect name of browser")
    else:
        print("User already exist edit data about it")

def edit_user():
    global user
    browser_list = ["chrome","edge","."]
    print(user)
    new_email = input("Write your email adres or . if you don't want change it : ")
    new_password = input ("Write your password or . if you don't want change it : ")
    new_browser = input ("Write your browser (chrome or firefox) or . if you don't want change it: ")
    browser = new_browser.lower()
    new_source = input ("Write your source or . if you don't want change it: ")
    if browser in browser_list:
        if browser !=".":
            user.browser = browser
    else:
        print("Uncorrect name of browser")
    if new_email !=".":
        user.email = new_email
    if new_password != ".":
        user.password = new_password
    if browser !=".":
        user.browser = browser
    if new_source != ".":
        user.source = new_source

def start_browser():
    if user.browser=="chrome":
        browser_path = r"\chromedriver.exe"
        PATH = user.source+browser_path
        driver = webdriver.Chrome(PATH)
    elif user.browser=="edge":
        browser_path = r"\msedgedriver.exe"
        PATH = user.source+browser_path
        driver = webdriver.Edge(PATH)

    return driver

def join_meeting(link, subject_name,start_time,day):
    print("Working")
    print("Scheduled class '%s' on %s at %s"%(subject_name,day,start_time))
    if subject_name == None:
        join_meeting_Zoom(link)
    else:
        join_meeting_Teams(subject_name,link)



def join_meeting_Zoom(link):
    print("Zoom")

    driver = start_browser()


    driver.get(link)
    time.sleep(15)
    driver.quit()

def join_meeting_Teams(subject_name,link):
    print("MS Teams")
    driver = start_browser()
    driver.get(link)
    log_in_btn= driver.find_element_by_id("mectrl_main_trigger")
    driver.implicitly_wait(5)
    log_in_btn.click()
    driver.implicitly_wait(5)
    #loging
    emailField = driver.find_element_by_xpath('//*[@id="i0116"]')
    emailField.click()
    emailField.send_keys(user.email)
    driver.find_element_by_xpath('//*[@id="idSIButton9"]').click() #Next button
    time.sleep(5)
    passwordField = driver.find_element_by_xpath('//*[@id="passwordInput"]')
    passwordField.click()
    passwordField.send_keys(user.password)
    driver.find_element_by_xpath('//*[@id="submitButton"]').click() #remember login
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="idSIButton9"]').click()
    time.sleep(14)


    #join class new function ??


    join_class(driver,subject_name)
    #driver.find_element_by_xpath('//*[@class="use-app-lnk"]').click()
def join_class(driver,subject_name):
    classes_available = driver.find_elements_by_class_name("name-channel-type")

    for i in classes_available:
    	if "cell biology" in i.get_attribute('innerHTML').lower():
    		print("JOINING CLASS ","cell biology")
    		i.click()
    		break
    try:
        joinbtn = driver.find_element_by_class_name("ts-calling-join-button")
        joinbtn.click()
        time.sleep(60)
    except:
        print("Meeting was cancel")
        return
            #to trzeba inaczej rozwiązać

    time.sleep(5)

    webcam = driver.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[2]/toggle-button[1]/div/button/span[1]')
    if(webcam.get_attribute('title')=='Turn camera off'):
        webcam.click()
        time.sleep(1)

        microphone = driver.find_element_by_xpath('//*[@id="preJoinAudioButton"]/div/button/span[1]')
    if(microphone.get_attribute('title')=='Mute microphone'):
        microphone.click()

        time.sleep(1)
        joinnowbtn = driver.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[1]/div/div/button')
        joinnowbtn.click()
def working_bot():
    '''days_of_week = {"monday":schedule.every().monday,
    "tuesday":schedule.every().tuesday,
    "wednesday":schedule.every().wednesday,
    "thursday":schedule.every().thursday,
    "friday":schedule.every().friday,
    "saturday":schedule.every().saturday,
    "sunday":schedule.every().sunday

    }
    '''
    for meeting in meetings:
        start_time = meeting.start_time
        link = meeting.link
        day = meeting.day_name
        subject_name = meeting.subject_name

        if day == "monday":
            schedule.every().monday.at(start_time).do(join_meeting,link, subject_name,start_time,day)
        elif day == "tuesday":
            schedule.every().tuesday.at(start_time).do(join_meeting,link, subject_name,start_time,day)
        elif day == "wednesday":
            schedule.every().wednesday.at(start_time).do(join_meeting,link, subject_name,start_time,day)
        elif day == "thursday":
            schedule.every().thursday.at(start_time).do(join_meeting,link, subject_name,start_time,day)
        elif day == "friday":
            schedule.every().friday.at(start_time).do(join_meeting,link, subject_name,start_time,day)
        elif day == "saturday":
            schedule.every().saturday.at(start_time).do(join_meeting,link, subject_name,start_time,day)
        elif day == "sunday":
            schedule.every().sunday.at(start_time).do(join_meeting,link, subject_name,start_time,day)

    while True:
        schedule.run_pending()
        time.sleep(1)




def check_time(time_input):
    time = time_input.split(":")
    try:
        time[0]=int(time[0])
        time[1]=int(time[1])
        print(time)

        if time[0]>=0 and time[0]<24 and time[1]>=0 and time[1]<60:
            return time_input
    except:
        print("Uncorrect time format")
        return None

def new_meeting():
    week = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    print("Create new meeting")
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    time_input = input("Start time meeting format 24h[00:00] : ")
    start_time = check_time(time_input)
    if start_time == None:
        return
    day = input("In what day you have meeting : ")
    if day.lower() in week:
        day_name = day.lower()
    else:
        print("This is not name of day")
    platform = input("This meeating will by on Zoom or MS Teams : ")
    if platform == "MS Teams":
        link = "https://www.microsoft.com/pl-pl/microsoft-teams/group-chat-software"
        subject_name = input("Subject name :  ")
        try:
            new_meeting = Meeting(start_time,day_name,link,subject_name.lower())
            print(new_meeting.start_time,new_meeting.link,new_meeting.subject_name)
            meetings.append(new_meeting)
            return

        except:
            print("Add  new meeting is not possible")
            return
    elif platform == "Zoom":
        link = input("Enter of link for meeting : ")
        try:
            new_meeting = Meeting(start_time,day_name,link)
        except:
            print("Add new meeting was't possible")
            return
    else:
        print("Adding meeting wasn't possible")
        return
    meetings.append(new_meeting)
    #print(new_meeting.start_time,new_meeting.link,new_meeting.subject_name)


def view_meetings():
    print("______________________________________________________")
    for meeting in meetings:
        print(meeting)

def find_meeting(time, day):
    for meeting in meetings:
        if meeting.day_name==day and meeting.start_time==time:
            return meeting
    print("You don't have meeting with this data")
    return None

def edit_meeting():
    week = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    print("Editing")
    print("______________________________________________________")
    start_time = input("Start Time : ")
    day_name = input("Day name : ")
    meeting = find_meeting(start_time,day_name)

    if meeting == None:
        return
    delete_or_not = input("If you want delete meeting write yes : ")
    if delete_or_not == "yes":
        meetings.remove(meeting)
        print("This meeting have been deleted")
        return

    start_time = input("Start time meeting format 24h[00:00] or . if you don't want change it: ")
    if start_time != ".":
        time=check_time(start_time)
        if time!=None:
            meeting.start_time = time
    day = input("In what day you have meeting or . if you don't want change it: ")
    if day.lower() in week:
        day_name = day.lower()
    else:
        print("This is not name of day")
    if day_name != ".":
        meeting.day_name = day_name
    meeting.day_name = day_name
    if meeting.link == "https://www.microsoft.com/pl-pl/microsoft-teams/group-chat-software":
        subject_name = input("Name of subject or . if you don't want change it : ")
        if subject_name != ".":
            meeting.start_time = subject_name
    else:
        link = input("If this link uccorrect and you want change it . if you don't want change it: ")
        if link !=".":
            meeting.link = link
def load_meetings(file_name):
    print('Loading meetings')
    global meetings
    with open(file_name,'rb') as input_file:
        meetings=pickle.load(input_file)



def save_meetings(file_name):
    print('Saving meetings')
    with open(file_name,'wb') as out_file:
        pickle.dump(meetings,out_file)
# I need change it later
def load_user(file_name):
    print('Loading meetings')
    global user
    with open(file_name,'rb') as input_file:
        user=pickle.load(input_file)

def save_user(file_name):
    print('Saving user')
    with open(file_name,'wb') as out_file:
        pickle.dump(user,out_file)
# Change to English
menu='''Bot do dołączania do spotkań

1. Nowe spotkanie
2. Wyświetl wszystkie
3. Edytuj spotkanie
4. Włącz bota
5.Edytuj dane użytkownika
6. Wyjście z programu
Wprowadź polecenie: '''

filename='meetings.pickle'
file_user='user.pickle'
try:
    load_meetings(filename)
    print("loading from file")
except:
    print("File with meetings don't exist")
    meetings=[]
try:
    load_user(file_user)
except:
    print("File with with user don't exist")
    user = None
    while user == None:
        print("Welcome to meeting bot aplication configure bot first")
        print("Write email and password for teams or leave empty if you don't youse MS Teams")
        print("________________________________________________________")
        new_user()
save_user(file_user)

while True:
    print("______________________________________________________")
    command = input(menu)

    if command=="1":
        new_meeting()
    elif command=="2":
        view_meetings()
    elif command=="3":
        edit_meeting()
    elif command=="4":
        working_bot()
    elif command=="5":
        edit_user()
    elif command=="6":
        save_meetings(filename)
        save_user(file_user)
        break
