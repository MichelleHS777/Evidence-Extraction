from tqdm import tqdm
import numpy as np
import statistics
import argparse

# ------------------------init parameters----------------------------
parser = argparse.ArgumentParser(description='Evaluate')
parser.add_argument('--gold_file', type=str, default='datasets/evidences/gold/gold_test.json', help='gold file')
parser.add_argument('--pred_file', type=str, default='datasets/evidences/semantic/semantic_test_th08_nofilter.json', help='predict file')
args = parser.parse_args()

pred_file = open(args.pred_file, 'r', encoding='utf-8')
gold_file = open(args.gold_file, 'r', encoding='utf-8')

precision = []
recall = []
f1 = []
count = 0
pred_output = 0
pred_std = []

for pred, gold in tqdm(zip(pred_file, gold_file), desc='Evaluating'):
    pred_evidences = eval(pred)['evidences']
    gold_evidences = eval(gold)['evidences']

    # gold & pred
    tp = 0
    for pred in pred_evidences:
        if pred in gold_evidences:
            tp += 1

    # len of pred is none
    if len(pred_evidences) == 0 and len(gold_evidences) != 0:
        each_precision = 0
        each_recall = 0
        # each_recall = tp / len(gold_evidences)

    # len of gold is none
    elif len(gold_evidences) == 0 and len(pred_evidences) != 0:
        # each_precision = tp / len(pred_evidences)
        each_precision = 0
        each_recall = 0
        count += 1
        continue

    # pred & gold all none
    elif len(pred_evidences) == 0 and len(gold_evidences) == 0:
        each_precision = 1
        each_recall = 1
        count += 1
        continue

    else:
        each_precision = tp / len(pred_evidences)
        each_recall = tp / len(gold_evidences)

    # calculate F1
    if each_precision == 0 and each_recall == 0:
        each_f1 = 0
    else:
        each_f1 = 2 * each_precision * each_recall / (each_precision + each_recall)

   # append each p, r, f1
    precision.append(each_precision)
    recall.append(each_recall)
    f1.append(each_f1)
    pred_output += len(pred_evidences)
    pred_std.append(len(pred_evidences))

# print('pred num:', pred_std)
std_deviation = statistics.stdev(pred_std)
print('Avg.:', pred_output/703, "；Standard Deviation:", std_deviation)

# avg of p, r, f1
precision = sum(precision) / len(precision)
recall = sum(recall) / len(recall)
f1 = sum(f1) / len(f1)
print("Precision: {:.2%}".format(precision))
print("   Recall: {:.2%}".format(recall))
print("       F1: {:.2%}".format(f1))
print('Drop:', count/999, 'count:', count)

