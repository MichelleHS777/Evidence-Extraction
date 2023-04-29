from tqdm import tqdm
import re
import json

dataset = json.load(open('./datasets/unpreprocess/dev.json', 'r', encoding='utf-8'))
save_file = open('./datasets/preprocessed/dev2.data', 'w', encoding='utf-8')


for data in tqdm(dataset, desc='Preprocess...'):
    claimId = data['claimId']
    claim = data['claim']
    label = data['label']
    evidences_doc = [data['evidence'][str(i)]['text'] for i in range(5)]
    gold_evidences = [data['gold evidence'][str(i)]['text'] for i in range(5)]
    for evidences_text in evidences_doc:
        for gold_evidences_text in gold_evidences:
            evidences_text = evidences_text.replace(gold_evidences_text, '')
        evidences_text = re.split(r'[？：。！（）.“”…\t\n]', evidences_text)
        evidences_text = [evidences for evidences in evidences_text if len(evidences)>5]
    for sent in evidences_text:
        save_file.write(claim + "\t" + sent + "\t" + str(0) + "\n")
    for gold_sent in gold_evidences:
        save_file.write(claim + "\t" + gold_sent + "\t" + str(1) + "\n")
save_file.close()
