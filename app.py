from flask import Flask ,render_template,request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/data', methods=['POST'])
def datafecth():
    user_inp=request.form.get('userinp')
    # 2. Initialize the Browser
    # chor    hide.add_arguments("--headless")
    chrome_option=Options()
    chrome_option.add_argument("--headless")
    chrome_option.add_argument("--disable-gpu")
    driver = webdriver.Chrome()

    try:
        # 3. Login Process
        driver.get("https://www.mlsmc.ac.in/signin.aspx")
        driver.implicitly_wait(10)
        
        driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_txtUname").send_keys(user_inp)
        driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_txtPwd").send_keys(user_inp)
        driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_btnLogin").click()
        
        # Give the dashboard a moment to load
        time.sleep(3) 
        
        # 4. Navigate to Profile
        driver.get("https://www.mlsmc.ac.in/student/editprofile.aspx")
        
        # Using the CSS Selector we discussed to avoid the ID $ vs _ issue
        profile_box = driver.find_element(By.CSS_SELECTOR, "input[id$='TextBox2']")
        extracted_value = profile_box.get_attribute("value")
        
        print(f"Extracted Value: {extracted_value}")

        # 5. Save to File
        with open('un_no.txt', 'a') as f:
            f.write(extracted_value)
        print("Value saved to un_no.txt")
        return render_template('index.html',result=extracted_value)
    except Exception as e :
        
        return render_template('index.html',result=f"can't connect to backend ! ! ! ${e} ")

    finally:
        # 6. Close the browser
        driver.quit()
if __name__ =='__main__':
    app.run()