import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# İstifadəçi adı və şifrəni əvvəlcədən daxil edirik
user_id = input("İstifadəçi adınızı daxil edin: ")
user_password = input("Şifrənizi daxil edin: ")

# WebDriver parametrləri
driver = webdriver.Chrome()

try:
    # Sayta daxil olma
    driver.get('https://sso.aztu.edu.az/')
    username = driver.find_element(By.NAME, "UserId")
    password = driver.find_element(By.NAME, "Password")

    # Daxil edilən istifadəçi adı və şifrəni yazırıq
    username.send_keys(user_id)
    password.send_keys(user_password)

    login_button = driver.find_element(By.XPATH, '/html/body/section/div/div[1]/div/div/form/div[3]/button')
    login_button.click()

    wait = WebDriverWait(driver, 30)

    # Tələbə keçid düyməsini klikləyirik
    telebe_kecid_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/aside[1]/div/nav/ul/li[1]/a')))
    telebe_kecid_button.click()

    # Fenlər düyməsini klikləyirik
    fenler_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menu6i"]/a/span[2]/span')))
    fenler_button.click()

    # Python dərsini seçirik
    python_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menu6i"]/ul/li[3]/a')))
    python_button.click()

    # Davamiyyət bölməsinə daxil oluruq
    davamiyyet_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main_content"]/div[1]/div/div[2]/a[7]')))
    davamiyyet_button.click()

    # Səhifənin tam yüklənməsini gözləyirik
    time.sleep(10)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Tarixləri və iştirak məlumatlarını tapırıq
    dates = soup.find_all('font', {'style': 'font-size:11px;'})  # Tarixlər
    attendance = soup.find_all('span', {'class': 'attend-label ie'})  # İştirak məlumatları

    # Nəticələri formatlanmış şəkildə çap edirik
    print("Davamiyyət Məlumatları:")
    print("-" * 30)
    for date, attend in zip(dates, attendance):
        status = "İştirak Edib" if attend.get_text().strip() == "i/e" else "İştirak Etməyib"
        print(f"Tarix: {date.get_text().strip()}, Status: {status}")

except Exception as e:
    print(f"Xəta baş verdi: {e}")
finally:
    driver.quit()
