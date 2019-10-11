#Author: Rich Magnotti
#Personal Project
#Purpose: simplify the process of making relevant connections as a new LinkedIn user

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
#**********************************************************************************************************************
#    Main driver function
#**********************************************************************************************************************
def main():
    driver = webdriver.Chrome('/usr/local/bin/chromedriver')  # driver is the browser
    driver.get("http://www.linkedin.com")  # navigate to a specific URL
    assert "Link" in driver.title  # verify a word is in the literal title of the website

    #find login text box and fill
    try:
        WebDriverWait(driver,50).until(
            EC.visibility_of_element_located((By.ID, "login-email")))
    finally:
        elem = driver.find_element_by_id("login-email")
    driver.execute_script('arguments[0].click();', elem)
    elem.send_keys("EXAMPLE_USER_NAME") #enter username here

    #find psswd text box and fill
    try:
        WebDriverWait(driver,50).until(
            EC.visibility_of_element_located((By.ID, "login-password")))
    finally:
        elem = driver.find_element_by_id("login-password")
    driver.execute_script('arguments[0].click();', elem)
    elem.send_keys("EXAMPLE_PASSWORD") #enter password here
    elem.submit()

    numCon = 20 #number of desired connection attempts
    #call the fn to complete the connection process

    searchCareerInterest(driver)

    # -------------------------------------------------------------------------------------------------------------
    #   LinkedIn sets a search quota. Once that quota is met, it blurs out almost all other connections.
    #
    #   This portion is the initial check to see if met quota or not.
    #   Member connecting is handles entirely differently if member quota met or not.
    # -------------------------------------------------------------------------------------------------------------
    # this try is to make sure at least 1 member is loaded before checking if any other members are blurred
    try:
        WebDriverWait(driver, 50).until(
            EC.visibility_of_element_located((By.XPATH, "//ul[contains(@class, "
                                                        "'search-results__list list-style-none')]"
                                                        "/li[%s]/div[1]/div[1]" % (1))))
    finally:
        print("")

    # check if any blurred members appear
    metQuota = driver.find_elements_by_xpath("//ul[contains(@class, "
                                             "'search-result search-result__profile-blur "
                                             "search-result--occlusion-enabled ember-view')]")

    Qval = len(metQuota)
    if Qval > -1:
        print("Quota met, calling appropriate functions. ")
        # call func for handling when quota met
        secondaryAdd(driver, numCon)

    elif Qval < -1:
        print('Quota not met! Calling appropriate functions. ')
        #when quota not met
        primaryAdd(driver, numCon)

    print("Met quota of desired connections.\nClosing program!")
    driver.close()  # to close the browser when finished

def searchCareerInterest(driver):
    # -------------------------------------------------------------------------------------------------------------
    #   Search by career interest
    # -------------------------------------------------------------------------------------------------------------
    # first go home to reset settings for next search
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "feed-tab-icon")))
    finally:
        elem = driver.find_element_by_id("feed-tab-icon")
    driver.execute_script('arguments[0].click();', elem)

    # to find and select the search bar
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, ".//*[@class='nav-search-typeahead']"
                                                        "/artdeco-typeahead-deprecated[1]"
                                                        "/artdeco-typeahead-deprecated-input[1]"
                                                        "/input[1]")))
    finally:
        elem = driver.find_element_by_xpath(".//*[@class='nav-search-typeahead']"
                                            "/artdeco-typeahead-deprecated[1]"
                                            "/artdeco-typeahead-deprecated-input[1]"
                                            "/input[1]")
    driver.execute_script('arguments[0].click();', elem)
    elem.clear()
    elem.send_keys("software")
    time.sleep(1)
    elem.send_keys(Keys.ENTER)

    # select option so only people are listed, not businesses
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, ".//*[@class='search-vertical-filter__"
                                                        "filter-item-button button-tertiary-medium-muted']")))
    finally:
        elem = driver.find_element_by_xpath(".//*[@class='search-vertical-filter__"
                                            "filter-item-button button-tertiary-medium-muted']")
    driver.execute_script('arguments[0].click();', elem)

def primaryAdd(driver, num):
    # **********************************************************************************************************************
    #   This func:
    #   1) goes home
    #   2) searches for desired career interest
    #   3) finds nth person in list of members
    #   4) determines if the member is a recruiter or regular member
    #   5) attempts to connect and send tailored message
    #   it repeats until desired num of connections made
    # **********************************************************************************************************************
    j = 1 #true counter for num profiles
    i = 1
    print("Num desired connections ", num)
    while j<num:
        time.sleep(3)
        print("iteration num ", i)

        searchCareerInterest(driver)

        # to verify that we haven't already tried to connect with them
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//ul[contains(@class, "
                                                            "'search-results__list list-style-none')]"
                                                            "/li[%s]/div[1]/div[1]/div[3]/div[1]/button[1]" % (i))))
        finally:
            elem = driver.find_element_by_xpath("//ul[contains(@class, "
                                                "'search-results__list list-style-none')]"
                                                "/li[%s]/div[1]/div[1]/div[3]/div[1]/button[1]" % (i))
        connTxt = str.lower(elem.text)
        print("Member status: ", connTxt)

        if 'connect' not in connTxt:
            print("Member is already connected, moving onto next.")
            i = i + 1
            continue

        # to choose nth profile from list of profiles
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//ul[contains(@class, "
                                                            "'search-results__list list-style-none')]"
                                                            "/li[%s]/div[1]/div[1]/div[2]/a[1]/h3[1]/span[1]"
                                                            "/span[1]" % (i))))
        finally:
            elem = driver.find_element_by_xpath("//ul[contains(@class, "
                                                "'search-results__list list-style-none')]"
                                                "/li[%s]/div[1]/div[1]/div[2]/a[1]/h3[1]/span[1]/span[1]" % (i))

        # if linkedin wont allow access to this member, move to next iteration of loop
        if 'Member' in elem.text:
            print("Cant access this member")
            i = i + 1
            continue

        # click on profile
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//ul[contains(@class, "
                                                            "'search-results__list list-style-none')]"
                                                            "/li[%s]/div[1]/div[1]/div[2]/p[1]" % (i))))
        finally:
            elem = driver.find_element_by_xpath("//ul[contains(@class, "
                                                "'search-results__list list-style-none')]"
                                                "/li[%s]/div[1]/div[1]/div[1]/a[1]/figure[1]"
                                                "/div[1]/div[1]/div[1]/div[1]" % (i))
        driver.execute_script('arguments[0].click();', elem)

        memTitle, flag = getTitle(driver)

        addMem(driver, memTitle)

        print("Attempted connection complete to member ", i, '\nCompleted profiles ', j)
        j=j+1
        i = i+1

def secondaryAdd(driver, num):
    #this func is in case this program uses up max. searches for the calendar period
    #this func will utilize an alternate method of finding/friending other members
    #find psswd text box and fill
    for i in range(num):
        # try:
        #     WebDriverWait(driver, 50).until(
        #         EC.visibility_of_element_located((By.XPATH, "//li-icon[contains(@class, 'logo-lockup-inverse')]")))
        # finally:
        #     elem = driver.find_element_by_xpath("//li-icon[contains(@class, 'logo-lockup-inverse")
        # driver.execute_script('arguments[0].click();', elem)
        # print("clicked on linkedin home icon")

        time.sleep(3)
        try:
            WebDriverWait(driver, 50).until(
                EC.visibility_of_element_located((By.ID, "mynetwork-tab-icon")))
        finally:
            elem = driver.find_element_by_id("mynetwork-tab-icon")
        driver.execute_script('arguments[0].click();', elem)
        print("clicked on network tab")

        time.sleep(3)

        try:
            WebDriverWait(driver, 50).until(
                EC.visibility_of_element_located((By.XPATH, "//ul[contains(@class, 'mn-pymk-list__cards')]"
                                                            "/li[1]/div[1]/a[1]/img[1]")))
        finally:
            elem = driver.find_element_by_xpath("//ul[contains(@class, 'mn-pymk-list__cards')]"
                                                "/li[1]/div[1]/a[1]/img[1]")
        driver.execute_script('arguments[0].click();', elem)
        print("clicked on member card")

        memTitle, flag = getTitle(driver)
        if flag == False:
            print('because flag found, moving to next iteration')
            #move back a page
            driver.execute_script("window.history.go(-1)")
            #regrab first person and click 'x' to remove from reommendeds
            try:
                WebDriverWait(driver, 50).until(
                    EC.visibility_of_element_located((By.XPATH, "//ul[contains(@class, 'mn-pymk-list__cards')]"
                                                    "/li[1]/div[1]")))
            finally:
                elem = driver.find_element_by_xpath("//ul[contains(@class, 'mn-pymk-list__cards')]"
                                                    "/li[1]/div[1]")
            hover = ActionChains(driver).move_to_element(elem)
            hover.perform()

            try:
                WebDriverWait(driver, 50).until(
                    EC.visibility_of_element_located((By.XPATH, "//ul[contains(@class, 'mn-pymk-list__cards')]"
                                                    "/li[1]/div[1]/button[1]")))
            finally:
                elem = driver.find_element_by_xpath("//ul[contains(@class, 'mn-pymk-list__cards')]"
                                                    "/li[1]/div[1]/button[1]")
            driver.execute_script('arguments[0].click();', elem)
            #WORKS!

            #refresh and move to next iteration
            driver.refresh()

            continue

        addMem(driver, memTitle)

        time.sleep(5)

def addMem(driver, memTitle):
    #once on the member's page, this func will complete the connection phase and return

    # find and copy member's name
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@class, 'pv-top-card-v2-section__info mr5')]"
                           "/div[1]")))
    finally:
        elem = driver.find_element_by_xpath("//div[contains(@class, 'pv-top-card-v2-section__info mr5')]"
                                            "/div[1]")
    memName = elem.text
    print("Text NAME reads:\n", memName)

    # this to grab just first name
    spaceVal = memName.find(' ')
    memName = list(memName)
    fName = memName[:spaceVal]
    fName = ''.join(fName)
    print("Just first name: ", fName)

    # -------------------------------------------------------------------------------------------------------------
    #   Find and click the "connect" button->select add note->write message
    # -------------------------------------------------------------------------------------------------------------
    time.sleep(3)
    connFound = driver.find_elements_by_xpath(".//*[@class='pv-s-profile-actions pv-s-profile-actions--"
                                                        "connect button-primary-large mr2 mt2']")
    print("len con = ", len(connFound))

    flag = False
    if len(connFound) > 0: #if member has 'connect' button
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, ".//*[@class='pv-s-profile-actions pv-s-profile-actions--"
                                                            "connect button-primary-large mr2 mt2']")))
        finally:
            elem = driver.find_element_by_xpath(".//*[@class='pv-s-profile-actions pv-s-profile-actions--"
                                                "connect button-primary-large mr2 mt2']")
        driver.execute_script('arguments[0].click();', elem)
    else: #if the member only has follow option and no 'connect' option -- will just follow, for now
        try:
            WebDriverWait(driver, 50).until(
                EC.visibility_of_element_located((By.XPATH, "//button[contains(@class, "
                                                            "'pv-s-profile-actions pv-s-profile-actions--follow "
                                                            "button-primary-large mr2 mt2')]")))
            flag = True
        finally:
            elem = driver.find_element_by_xpath("//button[contains(@class, "
                                                            "'pv-s-profile-actions pv-s-profile-actions--follow "
                                                "button-primary-large mr2 mt2')]")
        driver.execute_script('arguments[0].click();', elem)

    if flag == True:
        pass
    elif flag == False:
        # select add note option from pop up
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, ".//*[@class='button-secondary-large mr1']")))
        finally:
            elem = driver.find_element_by_xpath(".//*[@class='button-secondary-large mr1']")
        driver.execute_script('arguments[0].click();', elem)

        # to add text
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "custom-message")))
        finally:
            elem = driver.find_element_by_id("custom-message")

        rec = False  # in case member is a recruiter
        if 'recruit' in memTitle:
            rec = True
        print("Is recruitment in title? ", rec)

        elem.clear()  # to clear any placeholder text
        if rec == True:
            # subBox.send_keys("Connection Inquiry")
            #ONLY IF RECRUITER -- MORE FORMAL
            elem.send_keys("Hello %s.\n\nI am a motivated, hard working, fresh graduate with "
                           "extensive computational "
                           "physics experience. I would like to apply my "
                           "quantitative/computer skills to a software developer position.\n\n"
                           "Let's keep in touch about available positions in this field!\n" % (fName))
        else:
            # ONLY IF NOT RECRUITER -- MESSAGE MORE INFORMAL
            # subBox.send_keys("Connection Inquiry")
            # example of possible message for potential connection
            elem.send_keys("Hi %s, I am a recent physics graduate with interests in algorithms, and desktop and mobile "
                           "application development.\n\nI'd love to stay in touch since we share a passion for software "
                           "and computers!\n" % (fName))

        # -------------------------------------------------------------------------------------------------------------
        #   Locate 'send' button, click
        # -------------------------------------------------------------------------------------------------------------
        # to find description message box
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//button[contains(@class, 'button-primary-large ml1')]")))
        finally:
            elem = driver.find_element_by_xpath("//button[contains(@class, 'button-primary-large ml1')]")
        driver.execute_script('arguments[0].click();', elem)

def getTitle(driver):
    # -------------------------------------------------------------------------------------------------------------
    #   Locate verify member title -> locate and copy member first name
    # -------------------------------------------------------------------------------------------------------------
    # title
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h2[contains(@class, "
                                                        "'pv-top-card-section__headline mt1')]")))
    finally:
        elem = driver.find_element_by_xpath("//h2[contains(@class, "
                                            "'pv-top-card-section__headline mt1')]")
    memTitle = elem.text
    memTitle = str.lower(memTitle)  # to make title all lower case to make string matching easier
    print("Text TITLE reads:\n", memTitle)

    #dict/switch statement to compare against member title against acceptable terms
    switcher = ["tech", "software", "copmut", " it ", "dev", "engineer", "cyber", "security"]

    nameFlag = False
    for item in switcher:
        if item in memTitle: #if one of the accepted words is in the title
            print("Acceptable title ", item, " | Actual title ", memTitle)
            nameFlag = True

    print("Was a flag found? ", nameFlag)
    return memTitle,  nameFlag

if __name__ == '__main__':
    main()
