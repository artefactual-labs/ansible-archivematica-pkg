# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import os

#sqlite3 /var/archivematica/storage-service/storage.db "select  \`key\` FROM tastypie_apikey;"

class PyConfigureDashboard(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = os.getenv('AM_URL', 'http://192.168.0.128:81')
        self.storage_url = os.getenv('SS_URL', 'http://192.168.0.128:8001')
        self.storage_key = os.getenv('SS_API_KEY', '1234567')
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_py_configure_dashboard(self):
        driver = self.driver
        driver.get(self.base_url + "/installer/welcome/")
        driver.find_element_by_id("id_org_name").clear()
        driver.find_element_by_id("id_org_name").send_keys("test")
        driver.find_element_by_id("id_org_identifier").clear()
        driver.find_element_by_id("id_org_identifier").send_keys("test")
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys("test")
        driver.find_element_by_id("id_first_name").clear()
        driver.find_element_by_id("id_first_name").send_keys("test")
        driver.find_element_by_id("id_last_name").clear()
        driver.find_element_by_id("id_last_name").send_keys("test")
        driver.find_element_by_id("id_email").clear()
        driver.find_element_by_id("id_email").send_keys("test@test.es")
        driver.find_element_by_id("id_password1").clear()
        driver.find_element_by_id("id_password1").send_keys("test")
        driver.find_element_by_id("id_password2").clear()
        driver.find_element_by_id("id_password2").send_keys("test")
        driver.find_element_by_css_selector("button.btn.primary").click()
        time.sleep(90)
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.get(self.base_url + "/installer/storagesetup/")
        driver.find_element_by_id("id_storage_service_url").clear()
        driver.find_element_by_id("id_storage_service_url").send_keys(self.storage_url)
        driver.find_element_by_id("id_storage_service_apikey").clear()
        driver.find_element_by_id("id_storage_service_apikey").send_keys(self.storage_key)
        driver.find_element_by_name("use_default").click()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
