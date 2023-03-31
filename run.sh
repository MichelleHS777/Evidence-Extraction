python main.py --eval --test_data_path='datasets/preprocessed/train.json' --save_file='datasets/evidence/promptbert/prompt_train.json'
python main.py --eval --test_data_path='datasets/preprocessed/dev.json' --save_file='datasets/evidence/promptbert/prompt_dev.json'

python Semantic_Ranker.py  --test_data_path='datasets/preprocessed/train.json' --save_file='datasets/evidence/semantic/semantic_train.json'
python Semantic_Ranker.py  --test_data_path='datasets/preprocessed/dev.json' --save_file='datasets/evidence/semantic/semantic_dev.json'
