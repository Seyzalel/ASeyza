from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

driver = webdriver.Chrome(options=options)

try:
    driver.get("https://stresse.net/")
    wait = WebDriverWait(driver, 10)
    attack_hub_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.menu-link.btn.btn-primary.btn-round[href="/home"]')))
    actions = ActionChains(driver)
    actions.move_to_element(attack_hub_link).click().perform()
    wait.until(EC.title_contains("Login"))
    print("Todo o processo foi bem sucedido. A página redirecionada contém 'Login' no título.")
finally:
    driver.quit()
