import os.path
import random
import unittest

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class chrome_twitch_test(unittest.TestCase):

    def setUp(self):
        mobile_emulation = {
                "deviceMetrics": {"width": 1080, "height": 1920, "pixelRatio": 3.0},
                "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 ("
                             "KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"
        }

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        self.driver = webdriver.Chrome(options=chrome_options)

    def tearDown(self):
        self.driver.quit()

    def test_twitch_sequention(self):
        driver = self.driver
        driver.get('http://m.twitch.tv')
        self.assertIn("Twitch", driver.title)

        cookie = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-a-target='consent-banner-accept']")))
        assert cookie.is_displayed()
        cookie.click()

        searchButton = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/search']")))
        assert searchButton.is_displayed()
        searchButton.click()

        searchInput = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='search']")))
        assert searchInput.is_displayed()
        searchInput.send_keys(
            "StarCraft II")

        searchTitle = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//p[@title='StarCraft II']")))
        assert searchTitle.is_displayed()
        searchTitle.click()

        driver.execute_script("window.scrollTo(0, 250)")
        driver.execute_script("window.scrollTo(0, 250)")

        streamerNumber = random.randint(3, 9)
        streamer = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, f"(.//*[@class='tw-image'])[{streamerNumber}]")))
        assert streamer.is_displayed()
        streamer.click()

        try:
            consentClassification = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((
                By.XPATH,
                "//button[@data-a-target='content-classification-gate-overlay-start-watching-button']")))
        except TimeoutException:
            pass
        else:
            consentClassification.click()

        video = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[@data-a-target='video-ref']")))
        assert video.is_displayed()
        driver.save_screenshot('screenshot-desktop-chrome.png')

        assert os.path.exists('screenshot-desktop-chrome.png')

if __name__ == "__main__":
    unittest.main()
