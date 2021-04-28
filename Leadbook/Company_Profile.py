import Common_Module as cm


def profile_page(source_url):
    print('Company URL: ',source_url)
    profile_soup = cm.hit(source_url)
    soup_check = True
    while soup_check:
        if "Sorry, we're down for maintenance. :(" not in str(profile_soup):
            soup_check = False
        else:
            profile_soup = cm.hit(source_url)
    json_dict = dict()
    left_tab = profile_soup.find('div',{'class':'CompanyTopInfo_leftContentWrap__3gIch'})
    right_tab = profile_soup.findAll('div',{'class':'CompanyTopInfo_contentWrapper__2Jkic'})
    json_dict['company_name'] = left_tab.find('h1').text.strip()
    json_dict['company_location'] = ''.join([x.find('span',{'itemprop':'address'}).text for x in right_tab if 'address' in str(x)]).strip()
    json_dict['company_website'] = left_tab.find('div',{'itemprop':'url'}).text.strip()
    json_dict['company_webdomain'] = profile_soup.find('button',{'itemprop':'email'}).text.split('@')[1].strip()
    json_dict['company_industry'] = ''.join([x.find('span',{'class':'CompanyTopInfo_infoValue__27_Yo'}).text for x in right_tab if 'Industry' in str(x)]).strip()
    json_dict['company_employee_size'] = ''.join([x.find('span',{'class':'CompanyTopInfo_infoValue__27_Yo'}).text for x in right_tab if 'Head Count' in str(x)]).strip()
    json_dict['company_revenue'] = ''.join([x.find('span',{'class':'CompanyTopInfo_infoValue__27_Yo'}).text for x in right_tab if 'Revenue' in str(x)]).strip()
    json_dict['contact_details'] = list()
    contacts_soup = profile_soup.find('div', {'class': 'TopContacts_topContactList__lnim_'})
    for contact in contacts_soup.findAll('div',{'itemprop':'employee'}):
        contact_dict = dict()
        contact_dict['contact_name'] = contact.find('a',{'itemprop':'url'}).text
        contact_dict['contact_jobtitle'] = contact.find('p',{'itemprop':'jobTitle'}).text
        contact_dict['contact_email_domain'] = json_dict['company_webdomain']
        contact_url = contact.find('a',{'itemprop':'url'}).get('href')
        print('emp URL : ',contact_url)
        contact_soup = cm.hit(contact_url)
        contact_dict['contact_department'] = ''.join([x.find('span',{'class':'ContactTopInfo_infoValue__DNIWM'}).text
                                                      for x in contact_soup.findAll('div',{'class':'ContactTopInfo_contentWrapper__3VEQ2'}) if 'Department' in str(x)]).strip()
        json_dict['contact_details'].append(contact_dict)
    cm.json_write([json_dict],'company_profiles')
    return json_dict


if __name__ == '__main__':
    open('source_url.txt', 'a').close()
    company_file = cm.json.load(open('company_index.json', 'r'))
    for company in company_file:
        if not company['source_url'] in open('source_url.txt','r').read():
            profile_dict = profile_page(company['source_url'])
            profile_dict['source_url'] = company['source_url']
            profile_id = cm.Database(profile_dict).insert_company()
            contact_list = profile_dict['contact_details']
            [x.update({'profile_id' : profile_id}) for x in contact_list]
            for contact in contact_list:
                cm.Database(contact).insert_contact()
            with open('source_url.txt','a') as a:
                a.write(company['source_url']+'\n')






