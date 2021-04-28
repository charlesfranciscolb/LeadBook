# LeadBook Machine Test
<b>Overview:</b><br>
This task requires you to collect structured data from a website. You will be writing a web
crawler that will visit a website. Fetch html pages, parse them in the desired format and
save them in an output file.
You should use python language(Version 3.xx) for this programming task. Feel free to use
any framework/library(requests, selenium, scrapy etc.).

<br>NOTE: company_profiles.json will only contain a partial amount of the data as per requirement. The entire website is not advisable to scrape data from A-Z web pages since I do not have proxies to continuously hit the website. Hitting the website with standard IP address may lead to Legal Issues<br><br>

<b>Tools Used</b>:<br>
<ul>
  <li>Python Version 3.6 and above</li>
  <li>SQLite</li>
  <li>BeautifulSoup</li>
  <li>Table Plus - software to view DB (Download link - https://download.tableplus.com/windows/3.12.20/TablePlusSetup.exe)</li>  
</ul>

<b>Database - SQLite</b>:<br>
<ul>
  <li>SQLite is a very light weighted database so, it is easy to use it as an embedded software with devices like televisions, Mobile phones, cameras, home electronic devices, etc.</li>
  <li>Reading and writing operations are very fast for SQLite database. It is almost 35% faster than the File system.
</li>
  <li>SQLite is very easy to learn. You don't need to install and configure it. Just download SQLite libraries in your computer and it is ready for creating the database.
</li>
  <li>SQLite queries are smaller than equivalent procedural codes so, chances of bugs are minimal.
</li>  
  <li>SQLite database is accessible through a wide variety of third-party tools.
</li>

  
</ul>

<b>Requirements</b>:<br>
Go to Run and type 'cmd' and type the following:<br>
<b>
pip install bs4 <br>
pip install requests <br>
pip install html <br>
pip install unescape <br>
pip install sqlalchemy <b><br>
  
<b>Instructions:</b><br>
<ul>
  <li>Run the File "Listing_Script.py"</li>
  <li>Wait till execution completes</li>
  <li>Run the File "Company_Profile.py"</li>
</ul>

<b>Process and Architecture:</b><br>
<ul>
  <li>The File <b>Listing_Script.py</b> will extract Compnay Names and Source URL and save to JSON file <b>company_index.json</b></li>
  <li>The File <b>Company_Profile.py</b> will extract Compnay Names, Company Location, Company Website, Company Web domain, Company Industry, Company Employee Size, Company_Revenue and Contact Details (Contact Name, Contact Job title, Contact Email Domain, Contact Department) and save to JSON file <b>company_profiles.json</b></li>
  <li>The File <b>Company_Profile.py</b> will then push the Company Data (Compnay Names, Source URL, Company Location, Company Website, Company Web domain, Company Industry, Company Employee Size, Company_Revenue) to the Sqlite Database(<b>leadbook_db.db</b>) table <b>conmpany_profile</b> and Contact Data (Contact Name, Contact Job title, Contact Email Domain, Contact Department) to the Sqlite Database(<b>leadbook_db.db</b>) table <b>contact_details</b></li>
  <li>The table <b>contact_details</b> is mapped to the table <b>conmpany_profile</b>by storing the conmpany_profile.profile_id to the contact_details table</li>
  <li>Both Table are programmed to not import Duplicates</li>
</ul>
