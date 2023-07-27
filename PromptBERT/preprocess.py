from tqdm import tqdm
import re
import json
import os

def preprocess_predict_json(unpreprocess_file, save_file):
    dataset = open(unpreprocess_file, 'r', encoding='utf-8')
    save_file = open(save_file, 'w', encoding='utf-8')
    for data in tqdm(dataset, desc='Preprocess to predict file'):
        data = eval(data)
        claim = data['claim']
        doc = data['document']
        sentences = []
        for each_doc in doc:
            text = re.split(r'[？：。！（）.“”…\t\n]', each_doc)
            # get the sentences: not none and len > 5
            text = [evidences for evidences in text
                                if evidences != '' and len(evidences) > 5]
            sentences.extend(text)
        each_data = {'claim': claim, 'evidences': sentences}
        data = json.dumps(each_data, ensure_ascii=False)
        save_file.write(data + "\n")
    save_file.close()

def preprocess_predict(unpreprocess_file, save_file):
    dataset = json.load(open(unpreprocess_file, 'r', encoding='utf-8'))
    save_file = open(save_file, 'w', encoding='utf-8')
    for data in tqdm(dataset, desc='Preprocess to predict file'):
        claimId = data['claimId']
        claim = data['claim']
        label = data['label']
        sentences = []
        # get the gold evidence
        gold_evidences = [data['gold evidence'][str(i)]['text'] for i in range(5) if data['gold evidence'][str(i)]['text'] != '']
        # split document into sentences
        doc = [data['evidence'][str(i)]['text'] for i in range(5) if data['evidence'][str(i)]['text'] != '']
        for text in doc:
            # remove gold evidence in document
            for gold_evidence in gold_evidences:
                text = text.replace(gold_evidence, '')
            # split the sentence with punctuation
            text = re.split(r'[？：。！（）.“”…\t\n]', text) 
            # get the sentences: not none and len > 5
            text = [evidences for evidences in text
                            if evidences != '' and len(evidences) > 5]
            sentences.extend(text)
        each_data = {'claimId': int(claimId), 'claim': claim, 'evidences': gold_evidences + sentences, 'label': label}
        data = json.dumps(each_data, ensure_ascii=False)
        save_file.write(data + "\n")
    save_file.close()

def preprocess_train(unpreprocess_file, save_file):
    dataset = json.load(open(unpreprocess_file, 'r', encoding='utf-8'))
    save_file = open(save_file, 'w', encoding='utf-8')
    for data in tqdm(dataset, desc='Preprocess training data'):
        # write claim in file
        claim = data['claim']
        save_file.write(claim + "\n") 

        # write gold evidence in file
        gold_evidences = [data['gold evidence'][str(i)]['text'] for i in range(5) if data['gold evidence'][str(i)]['text'] != '']
        for gold in gold_evidences:
            save_file.write(gold + "\n")
        
        # split document into sentences
        sentences = []
        doc = [data['evidence'][str(i)]['text'] for i in range(5) if data['evidence'][str(i)]['text'] != '']
        for text in doc:
            # remove gold evidence in document
            for gold_evidence in gold_evidences:
                text = text.replace(gold_evidence, '')
            # split the sentence with punctuation
            text = re.split(r'[？：。！（）.“”…\t\n]', text) 
            # get the sentences
            text = [evidences for evidences in text
                    if evidences != '' and len(evidences) > 5]
            sentences.extend(text)
        # write sentences in file
        for sent in sentences:
            save_file.write(sent + "\n")
    save_file.close()
    

def main():
    # trian_path = './datasets/train2'
    # if not os.path.isdir(trian_path):
    #     os.mkdir(trian_path)
    # preprocess_train('./datasets/unpreprocess/train.json', 
    #                    './datasets/train2/train.data')
    
    # predict_path = './datasets/predict'
    # if not os.path.isdir(predict_path):
    #     os.mkdir(predict_path)
    # preprocess_predict('./datasets/unpreprocess/test.json', 
    #                    './datasets/predict/test.json')
    preprocess_predict_json('./doc_covid_date.json', './sent_covid_date.json')
    

if __name__ == "__main__":
    main()
