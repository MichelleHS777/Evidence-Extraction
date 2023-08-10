## Preprocess
    python preprocess.py 
`--dataset` set dataset path you want to preprocess     
`--save_file` set save path after preprocess 
## Training
    python main.py --train
* Train file: [link](https://drive.google.com/drive/folders/1aYMOnt617G5zrlsy6mgYhtQMsUbOw63M?usp=sharing)
## Predict Evidence 
    python main.py --eval --test_data_path='./datasets/predict/test.json' --save_file='./datasets/evidences/test_th08.json'
## Arguments 
`--train_data_path` (default='./datasets/train/train.json')  
`--test_data_path` (default='./datasets/predict/test.json')    
`--save_file` save file for threshold=0.8 (default='./datasets/evidences/SBERT_test.json')    
## Evaluate Evidence 
    python evalaute.py 
`--gold_file` set gold evidence path (default='datasets/evidences/gold/gold_test.json')    
`--pred_file` set predict path (default='datasets/evidences/semantic/semantic_test_th08_nofilter.json') 
## Checkpoint
* [Checkpoint](https://drive.google.com/drive/folders/1GTOh0e4krGQmEcdypIcNbstQ2ee591Ua?usp=sharing)
