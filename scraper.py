import requests
from bs4 import BeautifulSoup

url = "https://github.com/{}?tab={}"

def get_followers_or_following(handle, tab):
    """
    Fetches the followers or following list for a given handle.
    Maximum of 50 results are returned.

    For this project, I don't want to dfs() on handles with too many followers,
    so if the users has more than 100 followers, then this function returns []
    """
    try:
        r = requests.get(url.format(handle, tab))
        soup = BeautifulSoup(r.text, "html.parser")
        data = soup.find("main", {"id": 'js-pjax-container'}).findAll("div", {"class": 'd-table'})

        # Count of followers / following
        cnt = soup.find("a", {"class": 'Link--secondary no-underline no-wrap', "href": f"https://github.com/{handle}?tab={tab}"}).span.get_text(strip=True)
        cnt = int(cnt) if cnt.isdigit() else int(1e9)
        
        # If the user has too many followers or following, then return []
        if cnt > 100 or cnt <= 0:
            return []
        
        users_lst = []
        for row in data:
            if handle not in row.text:
                name = row.find("span", {"class": 'Link--primary'}).get_text(strip=True)
                if not name: name = None
                username = row.find("span", {"class": 'Link--secondary'}).get_text(strip=True)
                users_lst.append((username, name))
        return users_lst
    
    except Exception as e:
        print(e)
        return []


def get_followers(handle):
    return get_followers_or_following(handle, "followers")


def get_following(handle):
    return get_followers_or_following(handle, "following")


def get_full_name_from_handle(handle):
    try:
        r = requests.get(url.format(handle, "followers"))
        soup = BeautifulSoup(r.text, "html.parser")
        return soup.find("span", {"class": 'p-name vcard-fullname d-block overflow-hidden'}).get_text(strip=True)
    except:
        return handle

if __name__ == "__main__":
    print(get_followers("TheViking733n"))
    print(get_following("TheViking733n"))