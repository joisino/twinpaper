import pickle
import numpy as np


with open('twin_ids.pickle', 'rb') as f:
    weak = pickle.load(f)

with open('twin_papers.pickle', 'rb') as f:
    papers = pickle.load(f)

with open('self.pickle', 'rb') as f:
    self = pickle.load(f)

print('Including a Colon in the Title')
treat = []
control = []
for i, (a, b) in enumerate(weak):
    if ':' in papers[a]['title'] and ':' not in papers[b]['title']:
        treat.append(papers[a]['n_citation'])
        control.append(papers[b]['n_citation'])
    if ':' in papers[b]['title'] and ':' not in papers[a]['title']:
        treat.append(papers[b]['n_citation'])
        control.append(papers[a]['n_citation'])

print(format(np.mean(np.log2(treat) - np.log2(control)), '.3g'), len(treat))


print('Lengthen the Title')
treat = []
control = []
for i, (a, b) in enumerate(weak):
    if len(papers[a]['title']) > len(papers[b]['title']):
        treat.append(papers[a]['n_citation'])
        control.append(papers[b]['n_citation'])
    if len(papers[a]['title']) < len(papers[b]['title']):
        treat.append(papers[b]['n_citation'])
        control.append(papers[a]['n_citation'])

print(format(np.mean(np.log2(treat) - np.log2(control)), '.3g'), len(treat))


print('Lengthen the reference')
treat = []
control = []
for i, (a, b) in enumerate(weak):
    if len(papers[a]['references']) > len(papers[b]['references']):
        treat.append(papers[a]['n_citation'])
        control.append(papers[b]['n_citation'])
    if len(papers[a]['references']) < len(papers[b]['references']):
        treat.append(papers[b]['n_citation'])
        control.append(papers[a]['n_citation'])

print(format(np.mean(np.log2(treat) - np.log2(control)), '.3g'), len(treat))


print('Lengthen the abstract')
treat = []
control = []
for i, (a, b) in enumerate(weak):
    if 'indexed_abstract' in papers[a] and 'indexed_abstract' in papers[b]:
        if papers[a]['indexed_abstract']['IndexLength'] > papers[b]['indexed_abstract']['IndexLength']:
            treat.append(papers[a]['n_citation'])
            control.append(papers[b]['n_citation'])
        if papers[a]['indexed_abstract']['IndexLength'] < papers[b]['indexed_abstract']['IndexLength']:
            treat.append(papers[b]['n_citation'])
            control.append(papers[a]['n_citation'])

print(format(np.mean(np.log2(treat) - np.log2(control)), '.3g'), len(treat))


print('Lengthen the paper')
treat = []
control = []
for i, (a, b) in enumerate(weak):
    if 'page_start' in papers[a] and 'page_start' in papers[b]:
        try:
            page_a = int(papers[a]['page_end']) - int(papers[a]['page_start']) + 1
            page_b = int(papers[b]['page_end']) - int(papers[b]['page_start']) + 1
        except ValueError:
            continue
        if page_a > page_b:
            treat.append(papers[a]['n_citation'])
            control.append(papers[b]['n_citation'])
        if page_a < page_b:
            treat.append(papers[b]['n_citation'])
            control.append(papers[a]['n_citation'])

print(format(np.mean(np.log2(treat) - np.log2(control)), '.3g'), len(treat))


print('Self citation')
treat = []
control = []
for i, (a, b) in enumerate(weak):
    if a in self and b not in self:
        treat.append(papers[a]['n_citation'])
        control.append(papers[b]['n_citation'])
    if a not in self and b in self:
        treat.append(papers[b]['n_citation'])
        control.append(papers[a]['n_citation'])

print(format(np.mean(np.log2(treat) - np.log2(control)), '.3g'), len(treat))


print('Priority')
treat = []
control = []
for i, (a, b) in enumerate(weak):
    year_a = papers[a]['year']
    year_b = papers[b]['year']
    if year_a == year_b:
        continue
    cited_a = papers[a]['n_citation']
    cited_b = papers[b]['n_citation']
    if year_a > year_b:
        year_a, year_b = year_b, year_a
        cited_a, cited_b = cited_b, cited_a
    treat.append(cited_a)
    control.append(cited_b)

print(format(np.mean(np.log2(treat) - np.log2(control)), '.3g'), len(treat))
