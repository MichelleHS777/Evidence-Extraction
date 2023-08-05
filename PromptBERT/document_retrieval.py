from googlesearch import search
import requests
from bs4 import BeautifulSoup
import json
# ------------------------init parameters----------------------------
parser = argparse.ArgumentParser(description='Document Retrieval')
parser.add_argument('--save_file', type=str, default='doc_covid.json', help='save document result from google search')
parser.add_argument('--claim', type=str, default="COVID-19疫苗研發突破：輝瑞與BioNTech合作疫苗獲得顯著效果", help='a claim that you want to search')
parser.add_argument('--start_date', type=str, default="2020-01-01", help='starting date')
parser.add_argument('--end_date', type=str, default="2020-12-31", help='end date')
args = parser.parse_args()

save = open(args.save_file, 'a+', encoding='utf-8')
claim = args.claim
start_date = args.start_date
end_date = args.end_date
query = claim + " after:" + start_date + " before:" + end_date
results = search(query, stop=10, pause=2.0, lang="zh-tw")

# save search results 
evidences = []
for url in results:
	if 'news' in url or 'wiki' in url: # only get wiki/news urls
		print(url) # web url
		page = requests.get(url)
		soup = BeautifulSoup(page.content, "html.parser")
		evidence = soup.text.strip().replace('\n', '').replace(' ', '')
		evidences.append(evidence)
# save in json file
data = json.dumps({'claim': claim, 'document': evidences}, ensure_ascii=False)
save.write(data + "\n")
save.close()
