from tqdm import tqdm
import re
import json

dataset = json.load(open('./datasets/unpreprocess/dev.json', 'r', encoding='utf-8'))
save_file = open('./datasets/evidences_splitGold/dev.json', 'w', encoding='utf-8')


for data in tqdm(dataset, desc='Preprocess...'):
    claimId = data['claimId']
    claim = data['claim']
    label = data['label']
    evidences_doc = [data['evidences'][str(i)]['text'] for i in range(5)]
    gold_evidences = [data['gold evidences'][str(i)]['text'] for i in range(5)]
    for evidences_text in evidences_doc:
        for gold_evidences_text in gold_evidences:
            evidences_text = evidences_text.replace(gold_evidences_text, '')
        evidences_text = re.split(r'[？：。！（）.“”…\t\n]', evidences_text)
        evidences_text = [evidences for evidences in evidences_text if len(evidences)>5]
        data = json.dumps({'claimId': int(claimId), 'claim': claim, 'evidencess': evidences_text + gold_evidences, 'label': label}, ensure_ascii=False)
    save_file.write(data + "\n")
save_file.close()
