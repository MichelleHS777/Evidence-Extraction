from tqdm import tqdm
import re
import json

dataset = json.load(open('./datasets/dev.json', 'r', encoding='utf-8'))
save_file = open('./datasets/dev.json', 'w', encoding='utf-8')


for data in tqdm(dataset, desc='Preprocess...'):
    claimId = data['claimId']
    claim = data['claim']
    label = data['label']
    evidences_doc = [data['evidence'][str(i)]['text'] for i in range(5)]
    gold_evidences = [data['gold evidence'][str(i)]['text'] for i in range(5) if data['gold evidence'][str(i)]['text'] != '']
    for evidences_text in evidences_doc:
        for gold_evidences_text in gold_evidences:
            evidences_text = evidences_text.replace(gold_evidences_text, '')
        evidences_text = re.split(r'[？：。！（）.“”…\t\n]', evidences_text)
        evidences_text = [evidences for evidences in evidences_text if len(evidences) > 5]
    for gold in gold_evidences:
        data_hasEvidence = json.dumps({'claimId': int(claimId), 'claim': claim, 'evidences': gold, 'label': 1}, ensure_ascii=False)
        save_file.write(data_hasEvidence + "\n")
    for sent in evidences_text:
        data_noEvidence = json.dumps({'claimId': int(claimId), 'claim': claim, 'evidences': sent, 'label': 0}, ensure_ascii=False)
        save_file.write(data_noEvidence + "\n")
save_file.close()
