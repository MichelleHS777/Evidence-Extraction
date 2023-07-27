# PromptBERT-Evidence-Extraction
## Document Retrieval
    python document_retrieval.py  
`save` save evidence in file  
`claim` type the claim you want to search  
## Training
    python main.py --train
## Predict Evidence 
    python main.py --eval --test_data_path='datasets/predict/test.json' --save_file='datasets/evidences/promptbert/prompt_test.json'
## Arguments 
`--train_data_path` (default='./datasets/train/train.data')  
`--test_data_path` (default='./datasets/predict/test.json')    
`--save_file` save file for threshold=0.8 (default='./datasets/evidences/promptbert/prompt_test_claim_sent_th08.json')    
`--save_file_out5` save file for 5 evidence (default='./datasets/evidences/promptbert/prompt_test_claim_sent_out5.json')
