## Training
    python main.py --train
* train file: [link](https://drive.google.com/drive/folders/1aYMOnt617G5zrlsy6mgYhtQMsUbOw63M?usp=sharing)
## Predict Evidence 
    python main.py --eval --test_data_path='./datasets/test.json' --save_file='./datasets/test_th08.json'
## Arguments 
`--train_data_path` (default='./datasets/train/train.json')  
`--test_data_path` (default='./datasets/predict/test.json')    
`--save_file` save file for threshold=0.8 (default='./datasets/evidences/SBERT_test.json')    
