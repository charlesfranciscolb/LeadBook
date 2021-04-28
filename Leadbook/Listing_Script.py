import Common_Module as cm


def listing_page(page_data):
    listings = page_data.find('div', {'class': 'DirectoryList_seoDirectoryList__aMaj8'})
    if listings is not None:
        listy = [{'company_name': x.text, 'source_url': x.a.get('href')} for x in listings]
        cm.json_write(listy, 'company_index')


def main_page(soup_data):
    alphabets = [x.text.strip() for x in
                 soup_data.find('div', {'class': 'DirectoryTopInfo_alphabetLinkListWrapper__4a1SM'}).findAll('a')]
    for alphabet in alphabets:
        alpha_url = URL + alphabet
        print('Alphabet URL: ', alpha_url)
        next_page_condition = True
        while next_page_condition:
            alpha_soup = cm.hit(alpha_url)
            listing_page(alpha_soup)
            with open('alphaurl_log.txt', 'a') as a:
                a.write(alpha_url + '\n')
            next_page = alpha_soup.find('div', {'class': 'DirectoryList_actionBtnLink__Seqhh undefined'})
            if next_page is None:
                next_page_condition = False
                print('No Next Listing Page')
            else:
                alpha_url = next_page.find('a').get('href')
                print('Next Listing page: ', alpha_url)



if __name__ == '__main__':
    URL = "https://www.adapt.io/directory/industry/telecommunications/"
    first_hit = 'A'
    soup = cm.hit(URL + first_hit)
    main_page(soup)
