import requests
import pandas as pd
from tqdm import tqdm

community = "SluttyConfessions"
URL = f"https://www.reddit.com/r/{community}/new.json"
all_posts = []
after = None
headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

for i in tqdm(range(1000//100)):
	params = {'limit': 100, 'after': after}
	response = requests.get(URL, headers=headers, params=params)
	if response.status_code == 200:
		data = response.json()
		all_posts += data['data']['children']
		after = data['data']['after']
		if after is None:
			break
	else:
		print(f"Failed to get data. Status code: {response.status_code}")

dic = {
	"titles":[post['data']['title'] for post in all_posts],
	"text":[post['data']['selftext'] for post in all_posts],
	"num_comments": [post['data']['ups'] for post in all_posts],
	"upvote_ratio":[post['data']['upvote_ratio'] for post in all_posts],
	"ups":[post['data']['num_comments'] for post in all_posts],

	
}
data = pd.DataFrame(dic)
data['comments_per_upvotes'] = data['num_comments'] / data['ups']
data = data.sort_values(by=['num_comments', 'comments_per_upvotes','upvote_ratio', 'ups'], ascending=[False ,False, False, False])

data.to_excel(f"data_{community}.xlsx", mode="w", encoding='utf-8-sig', index=False)
print(f"Excel file exported successfully - contains {len(data)} lines")