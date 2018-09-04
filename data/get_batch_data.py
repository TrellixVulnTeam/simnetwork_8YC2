from data.data_utils import utt2id
import numpy as np

def dynamic_padding(corpus, token2id, pad_token="<PAD>", 
                    start_token=None, end_token=None):
    max_len = 0
    corpus_lst = []
    for utt in corpus:
        sent_lst = utt2id(utt, token2id, pad_token, start_token, end_token)
        corpus_lst.append(sent_lst)
        if max_len < len(sent_lst):
            max_len = len(sent_lst)

    for index, sent_lst in enumerate(corpus_lst):
        corpus_lst[index] += [token2id[pad_token]]*(max_len-len(sent_lst))
    return corpus_lst

def get_eval_batches(anchor, check, batch_size, 
                    token2id, is_training=True):
    if is_training:
        shuffled_index = np.random.permutation(len(anchor))
    else:
        shuffled_index = range(len(anchor))
    batch_num = int(len(anchor) / batch_size)
    end_index = 0
    for index in range(batch_num):
        start_index = index * batch_size
        end_index = start_index + batch_size

        sub_anchor = [anchor[t] for t in shuffled_index[start_index:end_index]]
        sub_check = [check[t] for t in shuffled_index[start_index:end_index]]

        anchor_lst = dynamic_padding(sub_anchor, token2id)
        check_lst = dynamic_padding(sub_check, token2id)

        anchor_lst = np.asarray(anchor_lst).astype(np.int32)
        check_lst = np.asarray(check_lst).astype(np.int32)

        yield anchor_lst, check_lst, []

    if end_index < len(anchor):

        sub_anchor = [anchor[t] for t in shuffled_index[end_index:]]
        sub_check = [check[t] for t in shuffled_index[end_index:]]

        anchor_lst = dynamic_padding(sub_anchor, token2id)
        check_lst = dynamic_padding(sub_check, token2id)

        anchor_lst = np.asarray(anchor_lst).astype(np.int32)
        check_lst = np.asarray(check_lst).astype(np.int32)

        yield anchor_lst, check_lst, []

def get_batches(anchor, check, label, batch_size, 
                    token2id, is_training=True):

    if is_training:
        shuffled_index = np.random.permutation(len(anchor))
    else:
        shuffled_index = range(len(anchor))
    batch_num = int(len(anchor) / batch_size)
    end_index = 0
    for index in range(batch_num):
        start_index = index * batch_size
        end_index = start_index + batch_size

        sub_anchor = [anchor[t] for t in shuffled_index[start_index:end_index]]
        sub_check = [check[t] for t in shuffled_index[start_index:end_index]]

        label_lst = [label[t] for t in shuffled_index[start_index:end_index]]
        anchor_lst = dynamic_padding(sub_anchor, token2id)
        check_lst = dynamic_padding(sub_check, token2id)

        label_lst = np.asarray(label_lst).astype(np.int32)
        anchor_lst = np.asarray(anchor_lst).astype(np.int32)
        check_lst = np.asarray(check_lst).astype(np.int32)

        yield anchor_lst, check_lst, label_lst

    if end_index < len(anchor):

        sub_anchor = [anchor[t] for t in shuffled_index[end_index:]]
        sub_check = [check[t] for t in shuffled_index[end_index:]]

        label_lst = [label[t] for t in shuffled_index[end_index:]]
        anchor_lst = dynamic_padding(sub_anchor, token2id)
        check_lst = dynamic_padding(sub_check, token2id)

        label_lst = np.asarray(label_lst).astype(np.int32)
        anchor_lst = np.asarray(anchor_lst).astype(np.int32)
        check_lst = np.asarray(check_lst).astype(np.int32)

        yield anchor_lst, check_lst, label_lst
