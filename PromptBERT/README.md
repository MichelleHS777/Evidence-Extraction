# PromptBERT-Evidence-Extraction
## Dataset
* [Train File Link](https://drive.google.com/drive/folders/1PzNUsgSIr9uuZAg0zOuFVQ6jAHxywcW_?usp=sharing)
## Document Retrieval
    python document_retrieval.py    
`--save_file` save documents in file (default='doc_covid.json')  
`--claim` type the claim you want to search (default='COVID-19疫苗研發突破：輝瑞與BioNTech合作疫苗獲得顯著效果')  
## Evidence Retrival
### Preprocess
* `preprocess_document` a function that preprocesses document from search results to sentences
* `preprocess_test_file` a function that get the evidence and non-evidence (save as `.data`)       
* `preprocess_train_file` a function that preprocesses train file into `json` (**claim, gold-evidence, non-evidence** (1 column))      
### Training
    python main.py --train
### Predict Evidence 
    python main.py --eval --test_data_path='datasets/predict/test.json' --save_file='datasets/evidences/promptbert/prompt_test.json'
### Arguments 
`--train` set if you want to train  
`--eval` set if you want to get the evidence   
`--train_data_path` train file is **.data** (default='./datasets/train/train.data')  
`--test_data_path` test file is **.json** (default='./datasets/predict/test.json')    
`--save_file` save file for threshold=0.8 (default='./datasets/evidences/promptbert/prompt_test_claim_sent_th08.json')    
`--save_file_out5` save file for 5 evidence (default='./datasets/evidences/promptbert/prompt_test_claim_sent_out5.json')
## Evaluate Evidence 
    python evalaute.py 
## Checkpoint
* [Checkpoint](https://drive.google.com/file/d/19LqR07hAHxODc4NcmEX2ONRP-yVEFPto/view?usp=sharing)
