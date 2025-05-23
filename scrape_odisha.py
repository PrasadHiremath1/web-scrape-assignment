
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # Comment this line to see the browser
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://rera.odisha.gov.in/projects/project-list")
time.sleep(5)
wait = WebDriverWait(driver, 10)

view_links = driver.find_elements(By.LINK_TEXT, "View Details")
print(f"Number of projects found: {len(view_links)}")

results = []

for i in range(min(6, len(view_links))):
    print(f"Opening project {i+1}")
    buttons = driver.find_elements(By.CSS_SELECTOR, "a.btn.btn-primary")
    if i >= len(buttons):
        print(f"Button index {i} out of range. Skipping.")
        continue
    driver.execute_script("arguments[0].scrollIntoView(true);", buttons[i])
    time.sleep(1)
    try:
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn.btn-primary")))
        driver.execute_script("arguments[0].click();", buttons[i])
    except Exception as e:
        print(f"Click failed: {e}")
        continue

    wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Promoter Details")))
    time.sleep(2)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "card-header")))

    try:
        project_name = driver.find_element(By.XPATH, "//label[contains(text(),'Project Name')]/following-sibling::strong").text.strip()
    except Exception as e:
        # print("DEBUG: Project Name not found:", e)
        project_name = "--"
    try:
        rera_regd_no = driver.find_element(By.XPATH, "//label[contains(text(),'RERA Regd. No.')]/following-sibling::strong").text.strip()
    except Exception as e:
        # print("DEBUG: RERA Regd. No. not found:", e)
        rera_regd_no = "--"

    print(f"Project Name: {project_name}")
    print(f"RERA Regd. No.: {rera_regd_no}")

    # Promoter tab
    try:
        promoter_tab = driver.find_element(
            By.XPATH, "//ul[contains(@class,'project-details-tab')]//a[normalize-space()='Promoter Details']"
        )
        driver.execute_script("arguments[0].click();", promoter_tab)
    except Exception as e:
        print("DEBUG: Promoter Details tab not found/clickable:")
        continue
    actions = ActionChains(driver)
    actions.move_to_element(promoter_tab).click().perform()

    time.sleep(5)

    
    try:
        WebDriverWait(driver, 15).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, ".ngx-overlay"))
        )
    except Exception:
        # print("DEBUG: Loader did not disappear in time, waiting extra 2 seconds.")
        time.sleep(2)

    def promoter_data_loaded(driver):
        try:
            el = driver.find_element(By.XPATH, "//div[contains(@class,'promoter')]//label[contains(text(),'Company Name')]/following-sibling::strong")
            print("DEBUG: Promoter Name field found, value:", el.text.strip())
            return el.text.strip() != ""
        except Exception as e:
            # print("DEBUG: Promoter Name not found yet:", e)
            return False

    try:
        WebDriverWait(driver, 20).until(promoter_data_loaded)
    except Exception as e:
        print("DEBUG: Promoter data did not load in time:")

    try:
        promoter_name = driver.find_element(
            By.XPATH, "//div[contains(@class,'promoter')]//label[contains(text(),'Company Name')]/following-sibling::strong"
        ).text.strip()
    except Exception as e:
        # print("DEBUG: Promoter Name not found:", e)
        promoter_name = "--"

    try:
        promoter_address = driver.find_element(
            By.XPATH, "//div[contains(@class,'promoter')]//label[contains(text(),'Registered Office Address')]/following-sibling::strong"
        ).text.strip()
    except Exception as e:
        # print("DEBUG: Registered Office Address not found:", e)
        promoter_address = "--"

    try:
        gst_no = driver.find_element(
            By.XPATH, "//div[contains(@class,'promoter')]//label[contains(text(),'GST No.')]/following-sibling::strong"
        ).text.strip()
    except Exception as e:
        # print("DEBUG: GST No. not found:", e)
        gst_no = "--"

    print(f"Promoter Name: {promoter_name}")
    print(f"Registered Office Address: {promoter_address}")
    print(f"GST No.: {gst_no}")

    driver.back()
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.btn.btn-primary")))

    results.append({
        "Porject Name": project_name,
        "RERA Regd. No.": rera_regd_no,
        "Promoter Name": promoter_name,
        "Registered Office Address": promoter_address,
        "GST No.": gst_no
    })
    
driver.quit()

with open("odisha_projects.html", "w", encoding="utf-8") as f:
    f.write("<html><head><title>Scraped Projects</title></head><body>")
    f.write("<h1>Scraped Projects</h1>")
    f.write("<table border='1'><tr><th>Project Name</th><th>RERA Regd. No.</th><th>Promoter Name</th><th>Registered Office Address</th><th>GST No.</th></tr>")
    for row in results:
        f.write(f"<tr><td>{row['Porject Name']}</td><td>{row['RERA Regd. No.']}</td><td>{row['Promoter Name']}</td><td>{row['Registered Office Address']}</td><td>{row['GST No.']}</td></tr>")
    f.write("</table></body></html>")
    
with open("odisha_projects.txt", "w", encoding="utf-8") as f:
    f.write("Project Name | RERA Regd. No. | Promoter Name | Registered Office Address | GST No.\n")
    f.write("-" * 100 + "\n")
    for row in results:
        f.write(f"{row['Porject Name']} | {row['RERA Regd. No.']} | {row['Promoter Name']} | {row['Registered Office Address']} | {row['GST No.']}\n")