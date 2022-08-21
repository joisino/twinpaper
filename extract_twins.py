import json
import pickle
from collections import defaultdict


def main():
    with open('dblp.v12.json') as f:
        dblp_json = json.loads(f.read())

    edges = set()
    twin = []
    for i, r in enumerate(dblp_json):
        if 'title' not in r or 'references' not in r:
            continue
        for e in r['references']:
            edges.add((r['id'], e))
            if (e, r['id']) in edges:
                twin.append((e, r['id']))

    appear = set(sum([list(a) for a in twin], []))

    papers = {}
    for i, r in enumerate(dblp_json):
        if r['id'] in appear:
            papers[r['id']] = r

    G = defaultdict(list)
    for i, r in enumerate(dblp_json):
        if 'authors' not in r:
            continue
        for a in r['authors']:
            for b in r['authors']:
                if a['id'] != b['id']:
                    G[a['id']].append(b['id'])
                    G[b['id']].append(a['id'])

    self = set()
    for i, r in enumerate(dblp_json):
        if 'references' not in r or 'authors' not in r:
            continue
        ra = set([a['id'] for a in r['authors']])
        for e in r['references']:
            if e in papers:
                if 'authors' not in papers[e]:
                    continue
                ea = set([a['id'] for a in papers[e]['authors']])
                if len(ra & ea) >= 1:
                    self.add(e)

    with open('twin_ids.pickle', 'wb') as f:
        pickle.dump(twin, f)

    with open('twin_papers.pickle', 'wb') as f:
        pickle.dump(papers, f)

    with open('coauthor.pickle', 'wb') as f:
        pickle.dump(G, f)

    with open('self.pickle', 'wb') as f:
        pickle.dump(self, f)


if __name__ == '__main__':
    main()
