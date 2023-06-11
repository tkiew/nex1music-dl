from bs4 import BeautifulSoup
import requests,re

def get_download_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    download_div = soup.find("div", class_="lnkdl animate")
    if download_div:
        download_links = download_div.find_all("a")
        return download_links
    else:
        return None


def search_music(query: str):
    formatted_query = query.replace(" ", "-")
    url = f"https://m.nex1music.ir/?s={formatted_query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    music_divs = soup.find_all('a', {'class': 'more'})
    links = []
    for div in music_divs:
        href = div.get('href')
        title = href.split('/')[-2].replace('-', ' ')
        links.append(href)
        print(f"{len(links)}: {title}")
    choice = int(input("\nشماره موزیک را وارد کنید:\n"))
    if not 1 <= choice <= len(links):
        return "شماره موزیک نامعتبر است."
    selected_link = links[choice-1]
    download_links = get_download_links(selected_link)
    if download_links:
        for i, link in enumerate(download_links):
            print(f"{i+1}: {link.text}\n")
        quality_choice = int(input("کدام کیفیت را می‌خواهید؟ \n"))
        if not 1 <= quality_choice <= len(download_links):
            return "کیفیت در دسترس نیست."
        download_link = download_links[quality_choice-1]["href"]
        filename = re.findall("filename=(.*)", download_link)[0].split("/")[-1].split(".")[0] + ".mp3"
        response = requests.get(download_link)
        with open(filename, "wb") as f:
            f.write(response.content)
        return f"با موفقیت دانلود شد.\nنام فایل:{filename}"
    else:
        return "لینک دانلود یافت نشد."


if __name__ == "__main__":
    print("\033[30;47mMade By Tkiew\033[0m\nTelegram ID : @SQLit\n\n")
    query = input('نام موزیک را وارد کنید: ')
    print(search_music(query))