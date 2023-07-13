from utils import *


class Usage:
    def __init__(self) -> None:
        self.driver = None
        self.cookies: List[dict] = None
        self.NOW: datetime.datetime = None
        self.NOW_MINUS_1_WEEK: datetime.datetime = None

    def _getCookies(self) -> List[dict]:

        self.NOW: datetime.datetime = datetime.datetime.today()
        self.NOW_MINUS_1_WEEK: datetime.datetime = self.NOW + datetime.timedelta(days=-6)

        COOKIES_FILES: list = glob.glob(f"../out/cookies/*.pkl")
        if len(COOKIES_FILES) > 1:
            for f_ in glob.glob("../out/cookies/*.pkl"):
                os.remove(f_)
            raise Exception("Too many cookies. Cleaning up")

        elif len(COOKIES_FILES) == 1:
            try:
                tmp = COOKIES_FILES[0].split("/")[-1].split(".")
                if len(tmp) != 2:
                    raise Exception("Bad filename: No dot (.) allowed within the filename")
                datetime_cookie, extension = datetime.datetime.strptime(tmp[0], "%Y-%m-%d"), tmp[1]
                if extension.lower() != "pkl":
                    raise Exception("Bad extension: Please provide a Pickle object")

                # If the stored cookies file is too old (older than 6 days), then proceed to the complete scraping
                if datetime_cookie < self.NOW_MINUS_1_WEEK:
                    # Proceed to the complete scraping (File to be updated)
                    os.remove(COOKIES_FILES[0])
                    return self._collectCookies()
                else:
                    # Read the pickle file
                    print("Reading the pickle file")
                    self.cookies = pickle.load(open(f"{COOKIES_FILES[0]}", "rb"))
                    return self.cookies
            except EOFError as e:
                raise Exception(f"Error: {e}")
        else:
            # Proceed to the complete scraping
            return self._collectCookies()

    def _collectCookies(self) -> List[dict]:
        options = Options()
        # options.add_argument(f"user-agent={USER_AGENT}")
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')

        self.driver = webdriver.Firefox()  # (options=options)
        # driver.minimize_window()
        self.driver.get(url=API_LOGIN_URL)

        try:
            # Clicking on "Sign In" button
            _ = WebDriverWait(driver=self.driver,
                              timeout=DELAY_SELENIUM).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()="Sign In With Github"]')))
            self.driver.find_element(by=By.XPATH,
                                     value='//button[text()="Sign In With Github"]').click()
        except TimeoutException:
            raise TimeoutException("Error")

        # Retrieving active tabs
        tabs = self.driver.window_handles
        self.driver.switch_to.window(tabs[1])

        try:
            # Logging in
            print("Logging ...")
            _ = WebDriverWait(driver=self.driver,
                              timeout=DELAY_SELENIUM).until(
                EC.presence_of_element_located((By.ID, 'login_field')))
            _ = WebDriverWait(driver=self.driver,
                              timeout=DELAY_SELENIUM).until(
                EC.presence_of_element_located((By.ID, 'password')))
            print(self.driver.current_url)
            self.driver.find_element(by=By.ID, value="login_field").send_keys(GH_USERNAME)
            self.driver.find_element(by=By.ID, value="password").send_keys(GH_PASSWORD)
            time.sleep(DELAY_SELENIUM)
            self.driver.find_element(by=By.ID, value="password").submit()
        except TimeoutException:
            raise TimeoutException("Error")

        # Checking endpoint URL
        attempt = 0
        while self.driver.current_url != API_ENDPOINT_AFTER_LOGIN:
            attempt += 1
            if attempt > LIMIT_ATTEMPT_AFTER_LOGIN:
                # TODO: Handle here the case where 'Reauthorization required'
                # TODO: Handle when github.com/session
                print(f"""
                                    {"-"*100}
                                    2 cases:
                                        - Accept the GitHub OAuth app (due to a high number of connections)
                                        - Enter the 2FA code (check your email)
                                    {"-"*100}
                                    """)
                # driver.maximize_window()
                time.sleep(1)
                attempt = 0
            time.sleep(0.05)
        print("Logging done...")

        # Getting cookies from session
        self.cookies = self.driver.get_cookies()

        # Closing window and destroying driver
        self.driver.close()
        self.driver.quit()

        # Saving cookies
        pickle.dump(self.cookies, open(f"../out/cookies/{self.NOW:%Y-%m-%d}.pkl", "wb"))

        return self.cookies

    def getUsage(self,
                 save: bool = True,
                 plot: bool = True) -> pd.DataFrame:

        if self.cookies is None \
                or (isinstance(self.cookies, list) and len(self.cookies) == 0) \
                or (isinstance(self.cookies, list) and len(self.cookies) > 1):
            self.cookies = self._getCookies()

        # API_POST_COOKIE: dict = [cookie for cookie in cookies if cookie["name"] == "aisstream-stream"][0]
        cookiesNames = list(map(itemgetter("name"), self.cookies))
        cookiesNames = dict(zip(cookiesNames, list(range(len(self.cookies)))))

        try:
            r = requests.post(url=API_USAGE_URL,
                              json={"type": "weekly"},
                              headers={
                                  "Referer": "https://aisstream.io/usage",
                                  "Origin": "https://aisstream.io",
                                  "Content-Type": "application/json",
                                  "Connection": "keep-alive",
                                  "User-Agent": USER_AGENT,
                              },
                              cookies={c: self.cookies[i]["value"] for c, i in cookiesNames.items()})

            if r.status_code != 200:
                raise Exception(f"An error has occurred.")
        except Exception as e:
            raise Exception(f"An error has occurred. ({e})")

        usage_data: List[dict] = r.json()["data"]

        df: pd.DataFrame = pd.DataFrame(data=usage_data)
        df["date"] = df["date"].str.replace(" +0000 UTC", "")
        df["date"] = pd.to_datetime(df["date"], format='%Y-%m-%d %H:%M:%S')
        df.rename(columns={"quantity": "messages"}, inplace=True)

        if save:
            print("On-disk saving...")
            df.to_csv(path_or_buf=f"../out/usages/{self.NOW:%Y-%m-%d}.csv", index_label="id")

        if plot:
            print("Plotting...")
            ax = df.plot.bar(x='date', y='messages', color='red', figsize=(15, 8), label="# of messages consumed")
            plt.xticks(ticks=list(df.index)[::5],
                       labels=[pd.to_datetime(k).strftime("%Y-%m-%d %H:%M:%S") for k in df['date'].to_numpy()[::5]],
                       rotation=45)
            plt.grid(visible=True)
            plt.gcf().subplots_adjust(bottom=0.25)
            plt.legend(loc="upper left", title="Labels")
            plt.xlabel("Date/Time")
            plt.ylabel("Messages consumed")
            plt.title("Messages consumed over the past 24 hours")
            plt.show()

        return df
