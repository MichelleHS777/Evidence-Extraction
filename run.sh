#python main.py --eval --test_data_path='datasets/preprocessed/train.json' --save_file='datasets/evidence/promptbert/prompt_train2.json'
#python main.py --eval --test_data_path='datasets/preprocessed/dev.json' --save_file='datasets/evidence/promptbert/prompt_dev2.json'
#python main.py --eval --test_data_path='datasets/preprocessed/test.json' --save_file='datasets/evidence/promptbert/prompt_test2.json'

 python Semantic_Ranker.py  --test_data_path='datasets/preprocessed/train.json' --save_file='datasets/evidence/semantic/semantic_train2.json'
 python Semantic_Ranker.py  --test_data_path='datasets/preprocessed/dev.json' --save_file='datasets/evidence/semantic/semantic_dev2.json'
 python Semantic_Ranker.py  --test_data_path='datasets/preprocessed/dev.json' --save_file='datasets/evidence/semantic/semantic_dev2.json'