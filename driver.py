
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import urllib.request
import img2pdf
import sys
import os


# Inputs: DropBox Url

if __name__ == "__main__":
    print(f"Arguments count: {len(sys.argv)}")
    usage = "python driver.py url num_slides"
    try:
        url = (sys.argv)[1]
        num_slides =int((sys.argv)[2])
        print(url)
    except IndexError:
        print("Invalid Input args")
        print(usage)
        sys.exit(1)
    
    try:
        path = (sys.argv)[3]
    except IndexError:
        path = "C:\\Users\\shahi\\Downloads\\"
    # get pdf name
    pdf_name = url.split('.pdf')[0][::-1].split('/')[0][::-1] + '.pdf'
    print(pdf_name)
    options = Options()
    options.headless = True
    driver = webdriver.Chrome('C:\dev\\bin\\chromedriver', options=options)
    driver.get(url)
    
    html = driver.find_element(By.TAG_NAME,'html')
    # html.send_keys(Keys.PAGE_DOWN)
    sleep(5)
    imgs = []
    for i in range(1, num_slides+1):
        while(True):
            try:
                print(i)
                img = driver.find_element(By.XPATH, f"(//img[@alt='{pdf_name}'])[{i}]")
                imgs.append(img)
                break
            except NoSuchElementException:
                html.send_keys(Keys.PAGE_DOWN)

    print(len(imgs))
    for i,img in enumerate(imgs):
        src = img.get_attribute('src')
        print(src)
        urllib.request.urlretrieve(src, f'{path}slide{i}.png')
        sleep(.5)
    # //img[@alt='Lec-1_Outline.pdf']

    # close driver
    driver.close()

    imgs =[f"{path}slide{i}.png" for i in range(num_slides)]
    
    # create pdf
    with open(f"{path}{pdf_name}", "wb") as f:
        f.write(img2pdf.convert(imgs))
    
    # purge image files
    for i in range(num_slides):
        os.remove(f"{path}slide{i}.png")