import pickle
import numpy as np

from collections import defaultdict
import queue

import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

np.random.seed(0)


def l1l1bow(a, b):
    la = sum([len(x) for x in a.values()])
    lb = sum([len(x) for x in b.values()])
    ma = defaultdict(float)
    for x, y in a.items():
        ma[x] = len(y) / la
    res = 0
    for x, y in b.items():
        res += min(ma[x], len(y) / lb)
    return 2 - 2 * res


with open('twin_ids.pickle', 'rb') as f:
    weak = pickle.load(f)

with open('twin_papers.pickle', 'rb') as f:
    papers = pickle.load(f)

with open('coauthor.pickle', 'rb') as f:
    G = pickle.load(f)


# Year Differences
year_diff = []
for a, b in weak:
    year_diff.append(np.abs(papers[a]['year'] - papers[b]['year']))

fig, ax = plt.subplots(figsize=(6, 4))

ax.hist(year_diff, range=(0, 10), bins=10, color='#005aff')
ax.tick_params(labelsize=14)

fig.savefig('imgs/year_diff.pdf')


# Distance of Abstracts
ds = []
for a, b in weak:
    if 'indexed_abstract' in papers[a] and 'indexed_abstract' in papers[b]:
        assert(len(papers[a]['indexed_abstract']['InvertedIndex']) > 0)
        assert(len(papers[b]['indexed_abstract']['InvertedIndex']) > 0)
        ds.append(l1l1bow(papers[a]['indexed_abstract']['InvertedIndex'], papers[b]['indexed_abstract']['InvertedIndex']))

rds = []
ids = list(papers.keys())
while len(rds) < len(ds):
    a, b = np.random.randint(len(papers), size=2)
    a, b = ids[a], ids[b]
    if 'indexed_abstract' in papers[a] and 'indexed_abstract' in papers[b]:
        rds.append(l1l1bow(papers[a]['indexed_abstract']['InvertedIndex'], papers[b]['indexed_abstract']['InvertedIndex']))

fig, ax = plt.subplots(figsize=(6, 4))

ax.hist([ds, rds], bins=20, color=['#005aff', '#ff4b00'], label=['twins', 'random'])

ax.tick_params(labelsize=14)
ax.legend(fontsize=14)

fig.savefig('imgs/topic_distance.pdf')


# Distance of Authors
def Gdist(a, b):
    goal = set([x['id'] for x in b])
    used = set()
    q = queue.Queue()
    for x in a:
        used.add(x['id'])
        q.put((0, x['id']))
    while not q.empty():
        cur = q.get()
        if cur[1] in goal:
            return cur[0]
        if cur[0] >= 3:
            return 3
        for nex in G[cur[1]]:
            if nex not in used:
                used.add(nex)
                q.put((cur[0] + 1, nex))
    return 3


for x in G.keys():
    G[x] = set(G[x])

ds = []
for i, (a, b) in enumerate(weak):
    if np.random.randint(100) != 0:
        continue
    if 'authors' in papers[a] and 'authors' in papers[b]:
        assert(len(papers[a]['authors']) > 0)
        assert(len(papers[b]['authors']) > 0)
        ds.append(Gdist(papers[a]['authors'], papers[b]['authors']))

rds = []
ids = list(papers.keys())
while len(rds) < len(ds):
    a, b = np.random.randint(len(papers), size=2)
    a, b = ids[a], ids[b]
    if 'authors' in papers[a] and 'authors' in papers[b]:
        rds.append(Gdist(papers[a]['authors'], papers[b]['authors']))

fig, ax = plt.subplots(figsize=(6, 4))

width = 0.4
ax.bar(np.arange(4) - width / 2, np.bincount(ds), width, color='#005aff', label='twin')
ax.bar(np.arange(4) + width / 2, np.bincount(rds), width, color='#ff4b00', label='random')
ax.set_xticks(np.arange(4))
ax.set_xticklabels(['0', '1', '2', '>=3'])

ax.tick_params(labelsize=14)
ax.legend(fontsize=14)

fig.savefig('imgs/community.pdf')
