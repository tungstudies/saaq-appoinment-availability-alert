import os
import time
from playsound import playsound
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from email_sender import send_email
from utils import ROOT_DIR, DRIVER_LICENCE_NO, TELEPHONE_NO, LANGELIER_POSTAL_CODE

TIMEOUT = 30  # (seconds)
CALLBACK_TIME = 60 * 5

# (minutes)


def check_appointment_unavailability():
    webdriver_path = os.path.join(ROOT_DIR, 'chromedriver', 'chromedriver.exe')
    browser = webdriver.Chrome(webdriver_path)

    target_url = 'https://saaq.gouv.qc.ca/en/online-services/citizens/driving-test/making-appointment/vehicule-class-5/'
    browser.get(target_url)

    wait = WebDriverWait(browser, TIMEOUT)
    access_button_xpath = '//*[@id="colonne-plugin-service-en-ligne"]/div[3]/a[1]'
    access_button = wait.until(EC.element_to_be_clickable((By.XPATH, access_button_xpath)))
    access_button.click()

    road_test_radio_xpath = '//*[@id="grpTypeExamen"]/div[2]/div[1]/label[1]/span[1]'
    road_test_radio = wait.until(EC.element_to_be_clickable((By.XPATH, road_test_radio_xpath)))
    road_test_radio.click()

    register_no_radio_xpath = '//*[@id="CoursPratiqueNon"]'
    register_no_radio = wait.until(EC.element_to_be_clickable((By.XPATH, register_no_radio_xpath)))
    register_no_radio.click()

    driver_licence_text_xpath = '//*[@id="Identification_Permis_NoPermis"]'
    driver_licence_text = wait.until(EC.element_to_be_clickable((By.XPATH, driver_licence_text_xpath)))
    driver_licence_text.send_keys(DRIVER_LICENCE_NO)

    telephone_number_text_xpath = '//*[@id="Identification_Telephone_Numero"]'
    telephone_number_text = wait.until(EC.element_to_be_clickable((By.XPATH, telephone_number_text_xpath)))
    telephone_number_text.send_keys(TELEPHONE_NO)

    next_button_xpath = '//*[@id="formulaire"]/div[1]/div[1]/div[1]/button[1]'
    next_button = wait.until(EC.element_to_be_clickable((By.XPATH, next_button_xpath)))
    next_button.click()

    is_langelier_postal_code = False
    while is_langelier_postal_code is False:
        search_button_xpath = '//*[@id="BoutonRechercher"]'
        search_button = wait.until(EC.element_to_be_clickable((By.XPATH, search_button_xpath)))
        search_text = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="Ville"]')))
        search_text.clear()
        search_text.send_keys(LANGELIER_POSTAL_CODE)
        search_button.click()
        time.sleep(3)

        first_box_postal_xpath = '//*[@id="block0"]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]'
        first_box_postal = wait.until(EC.element_to_be_clickable((By.XPATH, first_box_postal_xpath)))

        if str(first_box_postal.text).find(LANGELIER_POSTAL_CODE) > -1:
            print(first_box_postal.text)
            is_langelier_postal_code = True

    availabilities_button_xpath = '//*[@id="block0"]/div[1]/div[1]/div[1]/div[2]/button[1]'
    availabilities_button = wait.until(EC.element_to_be_clickable((By.XPATH, availabilities_button_xpath)))
    availabilities_button.click()

    error_message_box_content_xpath = '//*[@id="ConteneurMessagesSevere"]/div[1]/h3[1]'

    error_message_box_content = wait.until(EC.element_to_be_clickable((By.XPATH, error_message_box_content_xpath)))
    error_message = error_message_box_content.text

    error_details_xpath = '//*[@id="ConteneurMessagesSevere"]/div[1]/ul[1]/li[1]'
    error_details = wait.until(EC.element_to_be_clickable((By.XPATH, error_details_xpath)))
    error_details_text = error_details.text

    time.sleep(2)

    if str(error_message).find('error') != -1:
        is_error_found = True
        print('{} {}'.format(error_message, error_details_text))
        browser.quit()
    else:
        is_error_found = False
        print("There are appointments available at the moment")
    return is_error_found


if __name__ == '__main__':

    is_appointment_unavailable = True
    keep_running_program = True
    while keep_running_program:
        try:
            is_appointment_unavailable = check_appointment_unavailability()
            if is_appointment_unavailable is False:
                playsound('audio.mp3')
            time.sleep(CALLBACK_TIME)
        except:
            print("An exception occurred")
            playsound('audio.mp3')
            playsound('audio.mp3')
            # os.system("taskkill /f /im  chromedriver.exe")
            keep_running_program = False

