## Training
    python main.py --train
## Predict Evidence 
    python main.py --eval --test_data_path='datasets/predict/test.json' --save_file='datasets/evidences/promptbert/prompt_test.json'
## Arguments 
`--train_data_path` (default='./datasets/train/train.json')  
`--test_data_path` (default='./datasets/predict/test.json')    
`--save_file` save file for threshold=0.8 (default='./datasets/evidences/SBERT_test.json')    
