from tqdm import tqdm
import re
import json

dataset = open('./datasets/evidence/promptbert/prompt_test.json', 'r', encoding='utf-8')
save_file = open('./datasets/evidence/promptbert/prompt_test3.json', 'w', encoding='utf-8')


for data in tqdm(dataset, desc='Preprocess...'):
    data = eval(data)
    claimId = data['claimId']
    claim = data['claim']
    label = data['label']
    gold_evidences = data['evidences']
    if len(gold_evidences)==0:
        data = json.dumps({'claimId': int(claimId), 'claim': claim, 'evidences': ['', '', '', '', ''], 'label': label}, ensure_ascii=False)
    else:
        data = json.dumps({'claimId': int(claimId), 'claim': claim, 'evidences': gold_evidences, 'label': label},ensure_ascii=False)
    save_file.write(data + "\n")
save_file.close()
