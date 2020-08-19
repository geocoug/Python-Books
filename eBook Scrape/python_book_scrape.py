from bs4 import BeautifulSoup
import urllib.request
import requests
import os


ebook_pages = []
base_url = "https://www.slitherintopython.com/"

for i in range(1, 24):
    ebook_pages.append("https://www.slitherintopython.com/book/chapter_{0}/chapter_{0}.html".format(i))
ebook_pages.append("https://www.slitherintopython.com/book/chapter_23/solutions.html")


chapter = 1
for site in ebook_pages:
    print(site)
    page = requests.get(site)
    soup = BeautifulSoup(page.content, 'html.parser')

    for tag in soup.findAll(attrs={'class': 'content'}):
        tag['style'] = "padding-top:10px;"

    mycontent = soup.find("div", class_="content")

    print('  Downloading images')
    for img in mycontent.find_all('img'):
        if '../../assets' in img['src']:
            img_path = img['src'].replace('../../', '')
            img_dload = base_url + img_path
            print('    {}'.format(img_dload))
            img_url_parts = img_dload.split("/")
            img_name = img_url_parts[-1]
            urllib.request.urlretrieve(img_dload, 'assets/{}'.format(img_name))
            img['src'] = "./assets/{}".format(img_name)

    mystyles = soup.find_all("style")

    mycontent.find(id="mc_embed_signup").decompose()
    mycontent.find('a', class_="bmc-button").decompose()
    mycontent.find('a', class_="bmc-button").decompose()
    mycontent.find('h4').decompose()
    mycontent.find('h4').decompose()

    i=0
    for br in mycontent.find_all('br'):
        if i <= 2:
            mycontent.find('br').decompose()
        i += 1


    if chapter < 24:
        outfile = "chapter_{}.html".format(chapter)
    else:
        outfile = "solutions.html"

    for a in mycontent.find_all('a', href=True):           
        if a['href'] == "../chapter_{0}/chapter_{0}.html".format(chapter + 1):
            a['href'] = "./chapter_{}.html".format(chapter + 1)

        if a['href'] == "../chapter_{0}/chapter_{0}.html".format(chapter - 1):
            a['href'] = "./chapter_{}.html".format(chapter - 1)

    print('  Writing output file')
    with open(outfile, 'w+', encoding='utf-8') as f:
        f.write("<html>")
        f.write('<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css" integrity="sha384-GJzZqFGwb1QTTN6wy59ffF1BuGJpLSa9DkKMp0DgiMDm4iYMj70gZWKYbI706tWS" crossorigin="anonymous">')
        f.write("<head>")
        for style in mystyles:
            f.write(style.prettify())
        f.write("</head>")
        f.write(mycontent.prettify())
        f.write("</html>")

    chapter += 1
    print('')
