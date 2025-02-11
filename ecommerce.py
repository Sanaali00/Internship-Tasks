from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3

# Setup Selenium
options = Options()
options.add_argument("--headless")  # Run in background
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://www.amazon.in/s?i=electronics&bbn=1389401031&rh=n%3A1389401031&dc")

time.sleep(5)  # Allow time for page to load

products = driver.find_elements(By.CLASS_NAME, "a-link-normal")

for product in products[:10]:  # Limit to 10 products
    print(product.text, product.get_attribute("href"))

driver.quit()
data = {
    "Product Name": ["iPhone 13", "Samsung S21", "OnePlus 9", "Google Pixel 7"],
    "Price": [70000, 55000, 45000, 60000]
}

df = pd.DataFrame(data)

# 📊 Bar Chart of Product Prices
plt.figure(figsize=(10, 5))
plt.bar(df["Product Name"], df["Price"], color=["blue", "red", "green", "orange"])
plt.xlabel("Product")
plt.ylabel("Price (INR)")
plt.title("Product Prices on Amazon")
plt.xticks(rotation=45)
plt.show()
plt.figure(figsize=(7, 7))
plt.pie(df["Price"], labels=df["Product Name"], autopct="%1.1f%%", colors=["blue", "red", "green", "orange"])
plt.title("Price Distribution of Products")
plt.show()
conn = sqlite3.connect("amazon_products.db")
df = pd.read_sql_query("SELECT * FROM products", conn)
conn.close()

print(df)