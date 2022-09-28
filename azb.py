import sys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():
    # Check the number of arguments
    if len(sys.argv) != 4:
        print('Usage: azb.py [username/email] [password] [minimum feedback score]')
        sys.exit(1)

    # Get the username from the arguments
    my_username = sys.argv[1]

    # Get the password from the arguments
    my_password = sys.argv[2]

    # Get the feedback score from the arguments
    the_feedback_score = sys.argv[3]

    # Open the website
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get('https://www.ebay.ca/')

    # Find the navigation menu using the id
    navigation = driver.find_element(By.ID, 'gh-ul-nav')

    # Find the selling button in the navigation menu using the href that contains the word "MyeBayAllSelling"
    selling_button = navigation.find_element(By.CSS_SELECTOR, 'a[href*="MyeBayAllSelling"]')

    # Get the href attribute of the selling button
    selling_href = selling_button.get_attribute('href')

    # Open the selling page
    driver.get(selling_href)

    # login
    enter_login_info(driver, my_username, my_password)

    # Wait until overview page is loaded. If timeout, throw an exception
    try:
        WebDriverWait(driver, 300).until(lambda x: x.find_element(By.ID, "meb-items-cnt"))
    except:
        driver.quit()

    # Get the items hrefs
    hrefs = get_items_href(driver)
    users = []

    # Loop through all the items
    for item in hrefs:
        # Open the item page
        driver.get(item)

        # Wait until the item page is loaded by checking for an href that contains the work viewbids. If timeout, throw an exception
        try:
            WebDriverWait(driver, 300).until(lambda x: x.find_element(By.CSS_SELECTOR, 'a[href*="viewbids"]'))
        except:
            driver.quit()
        
        # Get the href attribute of the view bids button
        view_bids_href = driver.find_element(By.CSS_SELECTOR, 'a[href*="viewbids"]').get_attribute('href')

        # Open the view bids page
        driver.get(view_bids_href)

        # Wait until the bidder page is loaded by checking if the class app-bid-history__table exists. If timeout, throw an exception
        try:
            WebDriverWait(driver, 300).until(lambda x: x.find_element(By.CLASS_NAME, "app-bid-history__table"))
        except:
            driver.quit()
        
        # Get the bidder table
        bidder_table = driver.find_element(By.CLASS_NAME, 'app-bid-history__table')

        # Get all the href in the table
        hrefs = bidder_table.find_elements(By.TAG_NAME, 'a')

        # Add unique users by username and their feedback score to the list
        for href in hrefs:
            username = href.text.split('\\n')[-1]
            if username not in users:
                # get the feedback score and the href's sibling element
                feedback_score = href.find_element(By.XPATH, 'following-sibling::span').text

                # parse the feedback score in between paranthesis
                feedback_score = feedback_score[feedback_score.find('(')+1:feedback_score.find(')')]

                # add the user to the list
                users.append((username, feedback_score))

    # Print all the usernames and their feedback score, separated by a new line
    print('Found the following users: ')
    for user in users:
        print(user[0] + ', ' + user[1])

    # Get all usernames of the users with feedback score less than the_feedback_score and add them to a list if they are not already in the list
    usernames = []
    for user in users:
        if int(user[1]) < int(the_feedback_score):
            if user[0] not in usernames:
                usernames.append(user[0])

    # Go to https://www.ebay.com/bmgt/BuyerBlock?
    driver.get('https://www.ebay.com/bmgt/BuyerBlock?')

    # login
    enter_login_info(driver, my_username, my_password)

    # Wait until the page is loaded by checking if the element with id app-page-form-0 exists. If timeout, throw an exception
    try:
        WebDriverWait(driver, 300).until(lambda x: x.find_element(By.ID, "app-page-form-0"))
    except:
        driver.quit()

    # Get the textarea element
    textarea = driver.find_element(By.ID, 'app-page-form-0')

    # Get every username separated by commas in the textarea and add them to the usernames list
    for username in textarea.text.split(','):
        if username not in usernames:
            usernames.append(username)

    # Remove duplicates in the usernames list
    usernames = list(dict.fromkeys(usernames))

    # Print "The following users will be blocked: " and the unique usernames and their feedback score separated by new lines
    print('The following users will be added to the blocked bidders list: ')
    for user in users:
        if user[0] in usernames:
            print(user[0] + ', ' + user[1])

    # Clear the textarea
    textarea.clear()

    # Replace its content with the usernames and separate them by commas
    textarea.send_keys(','.join(usernames))

    # Find the button of type submit
    submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')

    # Click the submit button
    submit_button.click()

    # Print All Done!
    print('All Done!')

    # Close the browser
    driver.quit()

# get all the items' hrefs and return them
def get_items_href(driver):
    # List of all the items using the class pl-item
    items = driver.find_elements(By.CLASS_NAME, 'pl-item')

    # List of all the hrefs
    hrefs = []

    # Loop through all the items
    for item in items:
        # Get the item title in the page using the item id
        title = item.find_element(By.CLASS_NAME, 'item-title')

        # Get the href attribute inside the title item's child element
        href = title.find_element(By.TAG_NAME, 'a').get_attribute('href')

        # Add the href to the list
        hrefs.append(href)

    return hrefs

def enter_login_info(driver, my_username, my_password):
    # Wait until the username input is enabled. Timeout after 300 seconds. (Give time for recaptcha)
    try:
        WebDriverWait(driver, 300).until(lambda x: x.find_element(By.ID, "userid").is_enabled())
    except:
        driver.quit()
    
    # Find the username input using the id
    username_input = driver.find_element(By.ID, 'userid')

    # Enter the username
    username_input.send_keys(my_username)

    # Get the continue button using the id signin-continue-btn
    continue_button = driver.find_element(By.ID, 'signin-continue-btn')

    # Click the continue button
    continue_button.click()

    # Wait until the password input is enabled. Timeout after 10 seconds.
    password_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'pass'))
    )

    # Find the password input using the id pass
    password_input = driver.find_element(By.ID, 'pass')

    # Enter the password
    password_input.send_keys(my_password)

    # Get the sign in button using the id sgnBt
    sign_in_button = driver.find_element(By.ID, 'sgnBt')

    # Click the sign in button
    sign_in_button.click()

        
if __name__ == '__main__':
    main()
