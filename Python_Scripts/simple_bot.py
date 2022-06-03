#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import requests

# Global Variables
#url = "http://20.230.36.148:3000"
url = "http://juiceshop1.cloudteamapp.com"

credentials = {
    "email": "botfather@bots.corp",
    "password": "12345$",
    "sec_answer": "Botdauther",
}
address = {
    "country": "USA",
    "name": "Botfather",
    "mobile": "+1234567890",
    "zip_code": "12345",
    "address": "Street where the Bots live 1337",
    "city": "San Francisco",
}
payment = {
    "name": "Botfather",
    "cardnr": "5519010974980551",
    "month": "10",
    "year": "2080"
}

# Get all products on landing page and click on it.
def click_all_landingpage(browser):
    products = browser.find_elements(By.XPATH , '//div[@aria-label="Click for more information about the product"]')
    product_list = []
    for id in range(len(products)):
        products[id].location_once_scrolled_into_view
        products[id].click()
        element1 = WebDriverWait(browser, 200).until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Close Dialog"]')))
        element1.click()
        product_list.append(products[id].text)
    print("[+] Done clicking around on the Startpage")
    sleep(2)   

def create_account(browser, credentials):
    # Navigate to Login/Register Page
    browser.find_element(By.XPATH, '//button[@aria-label="Show/hide account menu"]').click()
    browser.find_element(By.XPATH, '//button[@id="navbarLoginButton"]').click()
    browser.find_element(By.LINK_TEXT, value = "Not yet a customer?").click()
    # Fill out register form
    browser.find_element(By.XPATH, '//input[@id="emailControl"]').send_keys(credentials["email"])
    browser.find_element(By.XPATH, '//input[@id="passwordControl"]').send_keys(credentials["password"])
    browser.find_element(By.XPATH, '//input[@id="repeatPasswordControl"]').send_keys(credentials["password"])
    browser.find_element(By.NAME,value="securityQuestion").click()
    ## Seems to be a highly dynamic value!!
    browser.find_element(By.ID, value="mat-option-3").click()
    browser.find_element(By.XPATH, '//input[@id="securityAnswerControl"]').send_keys(credentials["sec_answer"])
    sleep(0.3)
    element2 = browser.find_element(By.ID, value="registerButton")
    element2.click()
    # actions = ActionChains(browser)
    # actions.move_to_element(element2).perform()
    print("[+] Done Register a new account")
    sleep(2)

def login(browser, url, credentials):
    url = url + "/#/login"
    browser.get(url)
    browser.find_element(By.XPATH, '//input[@id="email"]').send_keys(credentials["email"])
    browser.find_element(By.XPATH, '//input[@id="password"]').send_keys(credentials["password"])
    browser.find_element(By.XPATH, '//button[@aria-label="Login"]').click()
    print("[+] Done login to the Webshop")
    sleep(2)

def add_new_address(browser, url, address):
    url = url + "/#/address/saved"
    browser.get(url)
    browser.find_element(By.XPATH, '//button[@aria-label="Add a new address"]').click()
    browser.find_element(By.XPATH, '//input[@data-placeholder="Please provide a country."]').send_keys(address["country"])
    browser.find_element(By.XPATH, '//input[@data-placeholder="Please provide a name."]').send_keys(address["name"])
    browser.find_element(By.XPATH, '//input[@data-placeholder="Please provide a mobile number."]').send_keys(address["mobile"])
    browser.find_element(By.XPATH, '//input[@data-placeholder="Please provide a ZIP code."]').send_keys(address["zip_code"])
    browser.find_element(By.XPATH, '//textarea[@id="address"]').send_keys(address["address"])
    browser.find_element(By.XPATH, '//input[@data-placeholder="Please provide a city."]').send_keys(address["city"])
    browser.find_element(By.XPATH, '//button[@id="submitButton"]').click()
    print("[+] Done adding a new address to the Webshop")
    sleep(2)

def add_new_payment(browser, url, payment):
    data = {
        "fullName": payment["name"],
        "cardNum": payment["cardnr"],
        "expMonth": payment["month"],
        "expYear": payment["year"]
    }
    token = browser.get_cookie("token")
    header = {
        "Authorization": "Bearer " + str(token["value"]),
        "Accept": "application/json" 
    }
    r = requests.post(url + "/api/Cards", headers=header, json=data)
    if r.status_code == 201:
        print("[+] Payment successfully added!")
    else:
        print(f"[-] ERROR Status: {str(r.status_code)}")
        print(f"[-] Error Text:\n{str(r.text)}")
    url = url + "/#/saved-payment-methods"
    browser.get(url)
    print("[+] Done adding a new payment method")
    sleep(2)
    
def add_items_shoppingcart(browser, url):
    browser.get(url)
    sleep(1)
    add_to_basket = browser.find_elements(By.XPATH , '//button[@aria-label="Add to Basket"]')
    for button in add_to_basket:
        button.location_once_scrolled_into_view
        button.click()
        sleep(2)
    print("[+] Done putting all available stuff into shoppingcart")
    sleep(2)

def checkout_shoppingcart(browser, url):
    browser.find_element(By.XPATH, '//button[@aria-label="Show the shopping cart"]').click()
    # need longer sleep as "item added..." popup is too slow
    sleep(5)
    element3 = WebDriverWait(browser, 200).until(EC.element_to_be_clickable((By.XPATH, '//button[@id="checkoutButton"]')))
    element3.location_once_scrolled_into_view
    element3.click()
    sleep(1)
    addresses = browser.find_elements(By.XPATH, '//mat-radio-button[@class="mat-radio-button mat-accent"]')
    addresses[0].click()
    browser.find_element(By.XPATH, '//button[@aria-label="Proceed to payment selection"]').click()
    sleep(1)
    delivery_speed = browser.find_elements(By.XPATH, '//mat-radio-button[@class="mat-radio-button mat-accent"]')
    delivery_speed[0].click()
    browser.find_element(By.XPATH, '//button[@aria-label="Proceed to delivery method selection"]').click()
    sleep(1)
    payment = browser.find_elements(By.XPATH, '//mat-radio-button[@class="mat-radio-button mat-accent"]')
    payment[0].click()
    browser.find_element(By.XPATH, '//button[@aria-label="Proceed to review"]').click()
    browser.find_element(By.XPATH, '//button[@aria-label="Complete your purchase"]').click()
    print("[+] Done placing order; selecting address, delivery & payment")
    browser.get(url)

# Initiate the browser, session & accept cookie banner
browser  = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
browser.maximize_window()
browser.get(url)
print("[*] Using URL: " + str(browser.current_url))
browser.find_element(By.CLASS_NAME , "cc-compliance").click()

click_all_landingpage(browser=browser)
create_account(browser=browser, credentials=credentials)
login(browser=browser, url=url, credentials=credentials)
add_new_address(browser=browser, url=url, address=address)
add_new_payment(browser=browser, url=url, payment=payment)
add_items_shoppingcart(browser=browser, url=url)
checkout_shoppingcart(browser=browser, url=url)

sleep(5)
browser.close()