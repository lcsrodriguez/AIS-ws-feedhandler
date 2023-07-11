import time

import matplotlib.pyplot as plt

from AIS import *

#asyncio.run(connect_ais_stream())

#options = Options()
#options.add_argument('--headless')
#options.add_argument('--disable-gpu')

driver = webdriver.Firefox() #(options=options)
driver.minimize_window()
driver.get(url=API_LOGIN_URL)

print("Logging ...")

try:
    # Clicking on "Sign In" button
    myElem = WebDriverWait(driver=driver,
                           timeout=DELAY_SELENIUM).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="Sign In With Github"]')))
    driver.find_element(by=By.XPATH,
                        value='//button[text()="Sign In With Github"]').click()
except TimeoutException:
    raise TimeoutException("Error")

# Retrieving active tabs
tabs = driver.window_handles
driver.switch_to.window(tabs[1])

try:
    # Logging in
    myElem = WebDriverWait(driver=driver,
                           timeout=DELAY_SELENIUM).until(
        EC.presence_of_element_located((By.ID, 'login_field')))
    myElem2 = WebDriverWait(driver=driver,
                            timeout=DELAY_SELENIUM).until(
        EC.presence_of_element_located((By.ID, 'password')))
    driver.find_element(by=By.ID, value="login_field").send_keys(GH_USERNAME)
    driver.find_element(by=By.ID, value="password").send_keys(GH_PASSWORD)
    time.sleep(1)
    driver.find_element(by=By.ID, value="password").submit()
except TimeoutException:
    raise TimeoutException("Error")

# Checking endpoint URL
attempt = 0
while driver.current_url != API_ENDPOINT_AFTER_LOGIN:
    attempt += 1
    if attempt > LIMIT_ATTEMPT_AFTER_LOGIN:
        print(f"""
        {"-"*100}
        2 cases:
            - Accept the GitHub OAuth app (due to a high number of connections)
            - Enter the 2FA code (check your email)
        {"-"*100}
        """)
        driver.maximize_window()
        time.sleep(1)
        attempt = 0
    time.sleep(0.05)

print("Logging done...")

# Getting cookies from msession
cookies = driver.get_cookies()

# Closing window and destroying driver
driver.close()
driver.quit()

#API_POST_COOKIE: dict = [cookie for cookie in cookies if cookie["name"] == "aisstream-stream"][0]
cookiesNames = list(map(itemgetter("name"), cookies))
cookiesNames = dict(zip(cookiesNames, list(range(len(cookies)))))

try:
    r = requests.post(url=API_USAGE_URL,
                      json={"type": "weekly"},
                      headers={
                          "Referer": "https://aisstream.io/usage",
                          "Origin": "https://aisstream.io",
                          "Content-Type": "application/json",
                          "Connection": "keep-alive",
                          "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
                      },
                      cookies={c: cookies[i]["value"] for c, i in cookiesNames.items()})

    if r.status_code != 200:
        raise Exception(f"An error has occurred.")
except Exception as e:
    raise Exception(f"An error has occurred. ({e})")

usage_data: List[dict] = r.json()["data"]

df: pd.DataFrame = pd.DataFrame(data=usage_data)
df["date"] = df["date"].str.replace(" +0000 UTC", "")
df["date"] = pd.to_datetime(df["date"], format='%Y-%m-%d %H:%M:%S')
df.rename(columns={"quantity": "messages"}, inplace=True)

print("On-disk saving...")

df.to_csv(path_or_buf="out.csv", index_label="id")

print("Plotting...")

ax = df.plot.bar(x='date', y='messages', color='red', figsize=(15, 8))
plt.xticks(ticks=list(df.index)[::5],
           labels=df["date"].to_numpy()[::5],
           rotation=45)
plt.grid(visible=True)
plt.gcf().subplots_adjust(bottom=0.25)
plt.xlabel("Date/Time")
plt.ylabel("Messages consumed")
plt.title("Messages consumed over the past 24 hours")
plt.show()
