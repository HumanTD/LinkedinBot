import re
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

EMAIL = ""
PASSWORD = ""


def initialize_webdrive() -> WebDriver:
    driver = webdriver.Firefox()
    driver.delete_all_cookies()
    driver.fullscreen_window()
    time.sleep(4)
    return driver


def login(driver: WebDriver, login_url: str) -> WebDriver:
    driver.get(login_url)
    time.sleep(5)
    email = driver.find_element(By.NAME, "session_key")
    email.send_keys(EMAIL)
    password = driver.find_element(By.NAME, "session_password")
    password.send_keys(PASSWORD)
    time.sleep(5)
    login_button = driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[1]/form/div[3]/button")
    try:
        login_button.click()
        time.sleep(20)

    except:
        print("Login Not working")
    return driver


def redirect(driver: WebDriver, url: str) -> WebDriver:
    driver.get(url)
    time.sleep(10)
    driver.find_element(By.CSS_SELECTOR,
                        "div#ember601.artdeco-dropdown.artdeco-dropdown--placement-bottom.artdeco-dropdown--justification-left")
    return driver


driver = initialize_webdrive()
driver = login(driver, "https://www.linkedin.com/login")
company_list = ["google"]

for company_name in company_list:
    print(company_name)
    # Replace with the name of the company you want to search
    driver.get(
        f"https://www.linkedin.com/search/results/companies/?keywords={company_name}&origin=SWITCH_SEARCH_VERTICAL"
    )

    try:
        # # Find the search box by XPath
        # search_box = driver.find_element(By.XPATH, "//input[@placeholder='Search' and @role='combobox' and @class='search-global-typeahead__input']")

        # wait = WebDriverWait(driver, 10)
        # search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search' and @role='combobox' and @class='search-global-typeahead__input']")))
        # search_box.click()

        # # Clear any existing text in the search box
        # search_box.clear()

        # # Enter the company name in the search box
        # search_box.send_keys(company_name)

        # # Press Enter to perform the search
        # search_box.send_keys(Keys.RETURN)
        # Wait for the search results page to load
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.reusable-search__result-container")))

        try:

            position = "swe"
            company_param = "google"
            people_search_url = f"https://www.linkedin.com/search/results/people/?currentCompany={company_param}&keywords={position}&origin=FACETED_SEARCH"

            driver.get(people_search_url)
            wait = WebDriverWait(driver, 20)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.reusable-search__result-container")))

            profile_parents = driver.find_elements(By.CSS_SELECTOR, "search-entity-result-universal-template")
            image_parents = driver.find_elements(By.CSS_SELECTOR, "div.entity-result__universal-image")
            profiles = driver.find_elements(By.CSS_SELECTOR, "li.reusable-search__result-container")
            print(len(profile_parents))
            print(len(image_parents))
            for profile in profiles:
                print(profile.text)

            for profile_parent, image_parent in zip(profile_parents, image_parents):
                profile_link = profile_parent.find_element(By.CSS_SELECTOR, "a.app-aware-link")
                print(profile_link.text)
                image_tag = image_parent.find_element(By.CSS_SELECTOR, "img.presence-entity__image")
                # Extract the src attribute
                pic_url = image_tag.get_attribute("src")
                print(profile_link.text)
                print(profile_link.get_attribute("href"))
                print()
        except NoSuchElementException:
            print("No search results found for the company.")

    except NoSuchElementException:
        print("Search box not found.")

    except TimeoutException:
        print("Timeout occurred while waiting for search results.")

# Close the browser
driver.quit()

# driver = initialize_webdrive()
# driver.get("https://www.linkedin.com/login")
# time.sleep(5)
# # Login
# email = driver.find_element(By.ID, "username")
# password = driver.find_element(By.ID, "password")
# login_btn = driver.find_element(By.XPATH, "/html/body/main/section[1]/div/div/form/div[2]/button")
# email.send_keys(EMAIL)
# password.send_keys(PASSWORD)
# login_btn.click()
#
# # Send connection request
# profile_url = "https://www.linkedin.com/in/nilaynathsharan/"
#
# try:
#     driver.get(profile_url)
#     time.sleep(10)
#     driver.find_element(By.CSS_SELECTOR, '[aria-label=Message]').click()
#
#     # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'artdeco-button artdeco-button--2 artdeco-button--primary ember-view pvs-profile-actions__action'))).click()
# except NoSuchElementException:
#     try:
#         driver.find_element(By.XPATH, '//button[contains(text(),"More")]').click()
#         WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.CLASS_NAME,
#                                         'artdeco-button artdeco-button--2 artdeco-button--primary ember-view pvs-profile-actions__action'))).click()
#     except NoSuchElementException:
#         print("Connect button not found.")
#
# # Wait and then quit the driver
# time.sleep(4)
# # driver.quit()
