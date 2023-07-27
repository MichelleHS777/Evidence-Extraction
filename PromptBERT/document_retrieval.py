from googlesearch import search
import requests
from bs4 import BeautifulSoup
import json

save = open('doc_covid_date.json', 'a+', encoding='utf-8')
start_date = "2020-01-01"
end_date = "2020-12-31"
claim = "COVID-19疫苗研發突破：輝瑞與BioNTech合作疫苗獲得顯著效果"
query = claim + " after:" + start_date + " before:" + end_date
# claim = 'NASA發現外星生命痕跡'
results = search(claim, stop=10, pause=2.0, lang="zh-tw")
evidences = []
for url in results:
	if 'news' in url or 'wiki' in url:
		# 網頁的網址
		print(url)
		page = requests.get(url)
		soup = BeautifulSoup(page.content, "html.parser")
		evidence = soup.text.strip().replace('\n', '').replace(' ', '')
		evidences.append(evidence)
data = json.dumps({'claim': claim, 'document': evidences}, ensure_ascii=False)
save.write(data + "\n")
save.close()
