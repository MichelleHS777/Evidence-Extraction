from tqdm import tqdm
import re
import json

dataset = json.load(open('./datasets/unpreprocess/test.json', 'r', encoding='utf-8'))
save_file = open('./datasets/evidences/gold_test.json', 'w', encoding='utf-8')


for data in tqdm(dataset, desc='Preprocess...'):
    claimId = data['claimId']
    claim = data['claim']
    label = data['label']
    gold_evidences = [data['gold evidences'][str(i)]['text'] for i in range(5)]
    data = json.dumps({'claimId': int(claimId), 'claim': claim, 'evidencess': gold_evidences, 'label': label}, ensure_ascii=False)
    save_file.write(data + "\n")
save_file.close()
