import time

from bs4 import BeautifulSoup as bs
import requests
from html import unescape
import json
import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, BigInteger, ForeignKey
from sqlalchemy import and_



class Database:
    def __init__(self, input_dict):
        self.engine = create_engine('sqlite:///leadbook_db.db').connect()
        self.meta = MetaData()
        self.profile = Table('conmpany_profile', self.meta,
                             Column('profile_id', BigInteger().with_variant(Integer, 'sqlite'), nullable=False,
                                    primary_key=True), Column('company_name', String),
                             Column('source_url', String), Column('company_location', String),
                             Column('company_website', String), Column('company_webdomain', String),
                             Column('company_industry', String), Column('company_employee_size', String),
                             Column('company_revenue', String), Column('contact_details', String))
        self.contacts = Table('contact_details', self.meta,
                              Column('contact_id', BigInteger().with_variant(Integer, 'sqlite'), nullable=False,
                                     primary_key=True), Column('contact_name', String),
                              Column('contact_jobtitle', String), Column('contact_email_domain', String),
                              Column('contact_department', String), Column('profile_id', Integer))
        self.meta.create_all(self.engine)
        self.input_dict = input_dict

    def insert_company(self):
        if_exist = [x for x in self.engine.execute(
            self.profile.select().where(self.profile.columns.source_url == self.input_dict['source_url']))]
        if len(list(if_exist)) == 0:
            self.engine.execute(self.profile.insert(), {'company_name': self.input_dict['company_name'],
                                                        'source_url': self.input_dict['source_url'],
                                                        'company_location': self.input_dict['company_location'],
                                                        'company_website': self.input_dict['company_website'],
                                                        'company_webdomain': self.input_dict['company_webdomain'],
                                                        'company_industry': self.input_dict['company_industry'],
                                                        'company_employee_size': self.input_dict['company_employee_size'],
                                                        'company_revenue': self.input_dict['company_revenue'],
                                                        'contact_details': str(self.input_dict['contact_details'])})
            id = [x for x in self.engine.execute(
                self.profile.select().where(self.profile.columns.source_url == self.input_dict['source_url']))]
            profile_id = id[0][0]
        else:
            profile_id = if_exist[0][0]
        return int(profile_id)

    def insert_contact(self):
        if_exist = [x for x in self.engine.execute(
            self.contacts.select().where(and_(self.contacts.columns.contact_name == self.input_dict['contact_name'],
                                         self.contacts.columns.contact_jobtitle == self.input_dict['contact_jobtitle'],
                                         self.contacts.columns.contact_email_domain == self.input_dict['contact_email_domain'],
                                         self.contacts.columns.contact_department == self.input_dict['contact_department'])))]
        if len(list(if_exist)) == 0:
            self.engine.execute(self.contacts.insert(), {'contact_name': self.input_dict['contact_name'],
                                                         'contact_jobtitle': self.input_dict['contact_jobtitle'],
                                                         'contact_email_domain': self.input_dict['contact_email_domain'],
                                                         'contact_department': self.input_dict['contact_department'],
                                                         'profile_id': self.input_dict['profile_id']})
        return


def json_write(json_data, name):
    print(str(json_data))
    name = name + '.json'
    if not os.path.exists(name):
        open(name, 'w')
    with open(name, 'r') as infile, open(name, 'r+') as outfile:
        try:
            old_data = infile.readline()
            old_data = json.loads(old_data)
            if str(json_data) not in str(old_data):
                data = old_data + json_data
                json.dump(data, outfile)
        except (json.JSONDecodeError, IndexError):
            json.dump(json_data, outfile)


def hit(url):
    iteration = 1
    condition = True
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"}
    while condition:
        try:
            response = requests.get(url, headers=header, timeout=10).text
            condition = False
            time.sleep(2)
        except requests.exceptions.ReadTimeout:
            print("Hit number:", iteration)
            iteration += 1
    return bs(unescape(response), 'html.parser')
