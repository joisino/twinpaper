import pickle
import numpy as np
from collections import defaultdict


id_to_name = {}
id_to_ind = {}


def venue_id(r):
    if 'venue' in r and 'id' in r['venue']:
        if 'raw' in r['venue']:
            id_to_name[r['venue']['id']] = r['venue']['raw']
        return r['venue']['id']
    return None


def venue_ind(i):
    if i not in id_to_ind:
        id_to_ind[i] = len(id_to_ind)
    return id_to_ind[i]


with open('twin_ids.pickle', 'rb') as f:
    weak = pickle.load(f)

with open('twin_papers.pickle', 'rb') as f:
    papers = pickle.load(f)

pair = defaultdict(list)
ind_res = []
for i, (a, b) in enumerate(weak):
    venue_a = venue_id(papers[a])
    venue_b = venue_id(papers[b])
    if venue_a == venue_b:
        continue
    cited_a = papers[a]['n_citation']
    cited_b = papers[b]['n_citation']
    if venue_a is not None and venue_b is not None:
        if venue_a > venue_b:
            venue_a, venue_b = venue_b, venue_a
            cited_a, cited_b = cited_b, cited_a
        pair[(venue_a, venue_b)].append(np.log2(cited_a) - np.log2(cited_b))
        a_ind = venue_ind(venue_a)
        b_ind = venue_ind(venue_b)
        ind_res.append((a_ind, b_ind))

ps = [(len(c), np.mean(c), a, b) for (a, b), c in pair.items() if a != b]
print(sorted(ps)[::-1][:10])
