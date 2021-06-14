from bs4 import BeautifulSoup
import requests

class Team:
    def __init__(self):
        self.list_team_urls = []
        self.base_url = "https://sofifa.com/teams?type=club"

    def get_team_urls(self, url=None):
        if(url is None):
            url = self.base_url
        self.fetch_team_urls(url)
        while(True):
            if(not self.is_next_page(url)):
                break
            else:
                url_next = self.is_next_page(url)
                print(f"Going to {url_next}")
                self.fetch_team_urls(url=url_next)
                url = url_next
        return

    def fetch_team_urls(self, url=None):
        if(url is None):
            url = self.base_url
        soup = BeautifulSoup(requests.get(url).content, "html.parser")
        table_body = soup.find("tbody")
        rows = table_body.find_all("tr")
        for row in rows:
            col = row.find_all("td")
            col = col[1]
            s = BeautifulSoup(str(col), features="html.parser")
            team_url = "https://sofifa.com" + s.find("td", {"class": "col-name-wide"}).find("a")["href"]
            self.list_team_urls.append(team_url)
        return

    def is_next_page(self, url):
        """Whether the next page button is available on the page
        """
        soup = BeautifulSoup(requests.get(url).content, "html.parser") 
        a_all = soup.find("div", {"class": "pagination"}).find_all("a")
        for a in a_all:
            href = a["href"]
            s = BeautifulSoup(str(a), features="html.parser")
            text = s.findAll(text=True)
            if("Next" in text):
                return("https://sofifa.com" + href)
        return(False)

if(__name__ == "__main__"):
    print("Hello")