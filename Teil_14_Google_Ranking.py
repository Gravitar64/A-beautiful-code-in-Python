import random
import arrow
from robobrowser import RoboBrowser

website = 'www.golem.de'
suchbegriffe = ['nachrichten+it','innovationen+it','neuigkeiten+it']
userAgents = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36']

jetzt = arrow.now().format('DD.MM.YYYY HH:mm:ss')

for suchbegriff in suchbegriffe:
  browser = RoboBrowser(history = False, user_agent=random.choice(userAgents),parser='html.parser')
  browser.open('https://www.google.de/search?num=500&q='+suchbegriff)
  links = browser.find_all('cite', {'class': 'iUh30'})
  gefundenePosition = 999
  for i, link in enumerate(links):
    if website in str(link):
      gefundenePosition = i+1
      break
  print(f'Position: {suchbegriff}, {gefundenePosition:03d}')
  with open('ranking_it.log', 'a') as f:
    f.write(f'{jetzt}, {gefundenePosition:03d}, {suchbegriff}\n')    
      
