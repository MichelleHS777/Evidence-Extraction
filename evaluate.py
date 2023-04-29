import torch
import re
from tqdm import tqdm


pred_file = open('datasets/prompt_test_claim2.json', 'r', encoding='utf-8')
gold_file = open('datasets/evidences/gold/gold_test.json', 'r', encoding='utf-8')


precision = []
recall = []
f1 = []
for pred, gold in tqdm(zip(pred_file, gold_file), desc='Evaluating'):
    id = eval(gold)['claimId']
    pred_evidences = eval(pred)['evidences']
    gold_evidences = eval(gold)['evidences']
    tp = 0
    for pred in pred_evidences:
        if pred in gold_evidences:
            tp += 1

    each_precision = tp / len(pred_evidences)
    each_recall = tp / len(gold_evidences)
    if each_precision == 0 and each_precision == 0:
        each_f1 = 0
    else:
        each_f1 = 2 * each_precision * each_recall / (each_precision + each_recall)
    precision.append(each_precision)
    recall.append(each_recall)
    f1.append(each_f1)

precision = sum(precision) / len(precision)
recall = sum(recall) / len(recall)
f1 = sum(f1) / len(f1)
print("Precision: {:.2%}".format(precision))
print("   Recall: {:.2%}".format(recall))
print("       F1: {:.2%}".format(f1))

