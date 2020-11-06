#! python
# multithreadXCKDDownloader.py - responsible for downloading all cartoons from XKCD, but now it's doing it in
# MULTITHREADING STYLE
# XI 2020 Arnold Cytrowski

import requests, os, bs4, threading
os.makedirs('xkcd', exist_ok=True)

def download_xkcd(startComic, endComic):
    for url in range(startComic, endComic + 1):
        print(f'downloading http://xkcd.com/{url}...')
        res = requests.get(f'http://xkcd.com/{url}')
        res.raise_for_status()

        soup = bs4.BeautifulSoup(res.text)

        comic_elem = soup.select('#comic img')
        if comic_elem == []:
            print('Sorry, can\'t find that cartoon')
        else:
            comic_url = comic_elem[0].get('src')
            print(f'Downloading {comic_url}...')
            res = requests.get(comic_url)
            res.raise_for_status()

            image_file = open(os.path.join('xkcd', os.path.basename(comic_url)), 'wb')
            for chunk in res.iter_content(10000):
                image_file.write(chunk)
            image_file.close()

download_threads = []
for i in range(0, 1400, 100):
    download_thread = threading.Thread(target=download_xkcd, args=(i, i + 99))
    download_threads.append(download_thread)
    download_thread.start()

for download_thread in download_threads:
    download_thread.join()
print('aaand it\'s done')
