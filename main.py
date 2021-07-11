import os
import json

from selenium import webdriver

from instagram import ig_login, ig_scraper
from _google import google_scraper


class InstagramScraper:

    def __init__(self):
        handles_list = []
        # handles.json contains usernames of 1000 influencers scraped from external website
        with open('handles.json', 'r') as fd:
            handles_data = json.loads(fd.read())
            handles = handles_data.get('objects') if type(handles_data) == dict else handles_data
            self.handles_data = handles
            last_item = handles_data.get('last') if type(handles_data) == dict else None
            for handle in handles:
                handle = handle['username']
                handles_list.append(handle)
            if last_item:
                handles_list = handles_list[
                    handles_list.index(last_item)+1:
                ]
        self.handles = handles_list

        self.driver_path = f'{os.getcwd()}/chromedriver'
        self.driver = webdriver.Chrome(self.driver_path)

        # Enter list of user credentials for instagram
        self.ig_users = [('<USERNAME>', '<PASSWORD>')]

    def restart_driver(self):
        if self.driver:
            self.quit_browser()
        self.driver = webdriver.Chrome(self.driver_path)

    def save_data(self, data):
        with open('data.json', 'r+') as wf:
            content = wf.read()
            if content:
                file_data = json.loads(content)
                file_data.append(data)
                wf.seek(0)
                json.dump(file_data, wf, indent=4)
            else:
                file_data = [data]
                wf.seek(0)
                json.dump(file_data, wf, indent=4)

    def run(self):
        start = 0
        uname, password = self.ig_users[start]
        ig_login(self.driver, uname, password)
        for i, handle in enumerate(self.handles):
            done = False
            try:
                print('Getting User: ', handle)
                influencer, status = ig_scraper(self.driver, handle)
                if status != 'ok':
                    if status == 'login':
                        if start+1 < len(self.ig_users):
                            start += 1
                            uname, password = self.ig_users[start]
                            # restart browser and login with new user
                            # if rate limit exceeded for current user
                            self.restart_driver()
                            ig_login(self.driver, uname, password)
                            self.handles.append(handle)
                            continue
                        else:
                            if i != 0:
                                self.add_last(self.handles[i-1])
                                break
                if influencer:
                    influencer.update(google_scraper(self.driver, handle))
                    self.save_data(influencer)
                    done = True
            except Exception as e:
                print(str(e))
                self.add_last(self.handles[i-1 if not done else i])
                break

        self.quit_browser()

    def quit_browser(self):
        self.driver.quit()

    def add_last(self, handle):
        with open('handles.json', 'w') as fd:
            new_data = {'objects': self.handles_data}
            new_data['last'] = handle
            fd.seek(0)
            json.dump(new_data, fd, indent=4)


if __name__ == '__main__':
    scraper = InstagramScraper()
    scraper.run()
