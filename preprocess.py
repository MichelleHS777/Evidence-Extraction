from tqdm import tqdm
import re
import json

dataset = json.load(open('./datasets/unpreprocess/test.json', 'r', encoding='utf-8'))
save_file = open('./datasets/preprocessed/test.json', 'w', encoding='utf-8')


for data in tqdm(dataset, desc='Preprocess...'):
    claimId = data['claimId']
    claim = data['claim']
    label = data['label']
    evidences = []
    evidences_doc = [data['evidence'][str(i)]['text'] for i in range(5) if data['evidence'][str(i)]['text'] != '']
    gold_evidences = [data['gold evidence'][str(i)]['text'] for i in range(5) if data['gold evidence'][str(i)]['text'] != '']
    for evidences_text in evidences_doc:
        for gold_evidences_text in gold_evidences:
            evidences_text = evidences_text.replace(gold_evidences_text, '')
        evidences_text = re.split(r'[？：。！（）.“”…\t\n]', evidences_text)
        evidences_text = [evidences for evidences in evidences_text
                          if evidences != '' and len(evidences) > 5]
        evidences.extend(evidences_text)
    each_data = {'claimId': int(claimId), 'claim': claim, 'evidences': gold_evidences + evidences, 'label': label}
    data = json.dumps(each_data, ensure_ascii=False)
    save_file.write(data + "\n")
save_file.close()
