import os
import json
import torch
import numpy as np
from tqdm import tqdm
from torch import nn
from config import set_args
from model_cls import Model
from torch.utils.data import DataLoader
import torch.nn.functional as F
from utils import compute_corrcoef, l2_normalize, compute_pearsonr
from transformers import AdamW, get_linear_schedule_with_warmup
from transformers.models.bert import BertTokenizer
from data_helper import load_data, SentDataSet, collate_func, convert_token_id

args = set_args()

def get_similar_sentence():
    dataset = open(args.test_data_path, 'r', encoding='utf-8')
    save = open(args.save_file, 'a+', encoding='utf-8')
    model.load_state_dict(torch.load(f"./checkpoint/train.ckpt"))
    model.eval()
    for data in tqdm(dataset, desc='getting similar sentence...'):
        data = eval(data)
        claimId = data['claimId']
        claim = data['claim']
        evidences = data['evidences']
        label = data['label']
        sent2sim = {}
        for ev_sent in evidences:
            if ev_sent in sent2sim:
                continue
            sent2sim[ev_sent] = cosSimilarity(claim, ev_sent, model, tokenizer)
        sent2sim = list(sent2sim.items())
        sent2sim.sort(key=lambda s: s[1], reverse=True)
        ev_sent = [s[0] for s in sent2sim[:5] if s[1] > 0.8]
        print(ev_sent)
        # ev_sent = [s[0] for s in sent2sim[:5]]
        data = json.dumps({'claimId': claimId, 'claim': claim, 'evidences': ev_sent, 'label': label}, ensure_ascii=False)
        save.write(data + "\n")
    save.close()


def cosSimilarity(sent1, sent2, model, tokenizer):
    model.eval()
    s1_input_ids, s1_mask, s1_segment_id = convert_token_id(sent1, tokenizer)
    s2_input_ids, s2_mask, s2_segment_id = convert_token_id(sent2, tokenizer)

    if torch.cuda.is_available():
        s1_input_ids, s2_input_ids = s1_input_ids.cuda(), s2_input_ids.cuda()

    with torch.no_grad():
        s1_embeddings = model.encode(s1_input_ids, encoder_type='last-avg')
        s2_embeddings = model.encode(s2_input_ids, encoder_type='last-avg')

    cos_sim = F.cosine_similarity(s1_embeddings, s2_embeddings)
    return cos_sim.item()


if __name__ == '__main__':
    args = set_args()
    args.output_dir = 'output_last-avg'
    os.makedirs(args.output_dir, exist_ok=True)
    tokenizer = BertTokenizer.from_pretrained(args.bert_pretrain_path)

    train_df = load_data(args.train_data_path)
    train_dataset = SentDataSet(train_df, tokenizer)
    train_dataloader = DataLoader(train_dataset, shuffle=True, batch_size=args.train_batch_size, collate_fn=collate_func)

    num_train_steps = int(len(train_dataset) / args.train_batch_size / args.gradient_accumulation_steps * args.num_train_epochs)

    # 模型
    model = Model()
    loss_fct = nn.CrossEntropyLoss()
    if torch.cuda.is_available():
        model.cuda()
        loss_fct.cuda()
    if args.train:
        param_optimizer = list(model.named_parameters())
        no_decay = ['bias', 'LayerNorm.bias', 'LayerNorm.weight']
        optimizer_grouped_parameters = [
            {'params': [p for n, p in param_optimizer if not any(nd in n for nd in no_decay)], 'weight_decay': 0.01},
            {'params': [p for n, p in param_optimizer if any(nd in n for nd in no_decay)], 'weight_decay': 0.0}
        ]

        warmup_steps = 0.05 * num_train_steps
        optimizer = AdamW(optimizer_grouped_parameters, lr=args.learning_rate, eps=1e-8)
        scheduler = get_linear_schedule_with_warmup(
            optimizer, num_warmup_steps=warmup_steps, num_training_steps=num_train_steps)

        for epoch in range(args.num_train_epochs):
            for step, batch in enumerate(train_dataloader):
                if torch.cuda.is_available():
                    batch = (t.cuda() for t in batch)
                s1_input_ids, s2_input_ids, label_id = batch
                if torch.cuda.is_available():
                    s1_input_ids, s2_input_ids, label_id = s1_input_ids.cuda(), s2_input_ids.cuda(), label_id.cuda()

                logits = model(s1_input_ids, s2_input_ids, encoder_type='last-avg')
                loss = loss_fct(logits, label_id)

                if args.gradient_accumulation_steps > 1:
                    loss = loss / args.gradient_accumulation_steps

                print('Epoch:{}, Step:{}, Loss:{:10f}'.format(epoch, step, loss))

                loss.backward()
                # nn.utils.clip_grad_norm(model.parameters(), max_norm=20, norm_type=2)   # 是否进行梯度裁剪

                if (step + 1) % args.gradient_accumulation_steps == 0:
                    optimizer.step()
                    scheduler.step()
                    optimizer.zero_grad()

            # 一轮跑完 进行eval
            # corrcoef, pearsonr = evaluate(model)
            # ss = 'epoch:{}, spearmanr:{:10f}, pearsonr:{:10f}'.format(epoch, corrcoef, pearsonr)
            # with open(args.output_dir + '/logs.txt', 'a+', encoding='utf8') as f:
            #     ss += '\n'
            #     f.write(ss)
            # model.train()

            model_to_save = model.module if hasattr(model, 'module') else model  # Only save the model it-self
            # output_model_file = os.path.join(args.output_dir, "epoch{}_ckpt.bin".format(epoch))
            torch.save(model_to_save.state_dict(), f'./checkpoint/train.ckpt')

    # Evaluate
    if args.eval:
        # Get similar sentence
        cossim = get_similar_sentence()