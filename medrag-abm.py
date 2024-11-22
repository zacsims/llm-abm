from src_.medrag import MedRAG
import ast
import re

medrag = MedRAG(llm_name="Google/gemini-1.5-flash-exp-0827", retriever_name=None)
'''
cell_types = ['cancer associated fibroblasts (CAFs)', 'Macrophages', 'Monocytes', 'CD4+ T Cells', 'CD8+ T Cells', 'Neoplastic Epithelium']
signals = ['Ncam1',
 'Col4a2',
 'Thbs3',
 'Vegfb',
 'Ccl6',
 'ITGA4_ITGB1',
 'Tnxb',
 'Lamb1',
 'Lama2',
 'Col9a3',
 'Lgals9',
 'Osm',
 'Pdgfa',
 'Sema3d',
 'Tgfb2',
 'Icam1',
 'Ccl2',
 'Ccl3',
 'Tnn',
 'Postn',
 'Tnc',
 'ITGAV_ITGB1',
 'Cdh1',
 'Vegfa',
 'Ccl9',
 'App',
 'Lamb2',
 'Ccl7',
 'Pros1',
 'Ccl8',
 'Ptprc',
 'Hspg2',
 'Tnf',
 'Nectin3',
 'Wnt5a',
 'Sema5a',
 'Tgfb3',
 'Fgf7',
 'Col6a2',
 'Sema3c',
 'Cxcl12',
 'Ptn',
 'Cxcl16',
 'Nampt',
 'Cd55',
 'Igf1',
 'Lama4',
 'C3',
 'Mdk',
 'Ccl12',
 'Csf1',
 'Igfbp3',
 'Thbs2',
 'F11r',
 'Col6a1',
 'Thy1',
 'Angptl4',
 'Efnb2',
 'Jam3',
 'Sdc2',
 'Cldn3',
 'Apoe',
 'Col1a1',
 'Col4a5',
 'Agrn',
 'Cadm1',
 'Mpzl1',
 'Efna5',
 'Angptl2',
 'Lair1',
 'Hbegf',
 'Sema3b',
 'Cd6',
 'Fn1',
 'Lpar1',
 'Jag1',
 'Gja1',
 'Gas6',
 'Areg',
 'Tenm3',
 'Sdc1',
 'Efnb1',
 'Cdh2',
 'Col4a1',
 'Thbs1',
 'Lamb3',
 'Mif',
 'Flrt2',
 'Ccl4',
 'Tnfsf12',
 'Tgfb1',
 'Lamc1',
 'Kitl',
 'Spp1',
 'Col6a3',
 'Cd86',
 'Col1a2']
'''
cell_types = ['CD8+ T Cells', 'CD8+ Naive T Cells', 'Exhausted T Cells', 'M0 Macrophages', 'M1 Macrophages', 'M2 Macrophages',  'Malignant Epithelial Cells']
signals = ['IL-10', 'IFN‐gamma']
 
k = 10
cell_type = "CD8+ T Cells"
signal="IL-10"
snippet_path_100 = f'/mnt/scratch/MedRAG/abm-rules-MedCPT-k={k}/{cell_type}_{signal}_snippets.json'
import json
def load_json(fpath):
    with open(fpath, 'r') as j:
        return json.loads(j.read())
    
snippets = load_json(snippet_path_100)
#snippets = [snippets[1], snippets[2]]
#snippets = [snippets[1]]
#snippets = [snippets[1], snippets[2], snippets[5]]
def add_pmids(explanation, snippets):
    doc_refs = re.findall('Document \[[0-9][0-9]?\]', explanation)
    if len(doc_refs) > 0:
        for doc_ref in doc_refs:
            idx = int(doc_ref[doc_ref.index('[')+1:doc_ref.index(']')])
            try:
                explanation = explanation.replace(doc_ref, f"PMID={snippets[idx]['PMID']}")
            except IndexError:
                print(f"tried to retrieve document [{idx}] PMID, but got list out of range, num_snippets={len(snippets)}")
                print(explanation)
    return explanation
import time
for k_ in range(5,31):
    for i in range(100):
        for cell_type in cell_types:
            for signal in signals:
                query = f"{signal} {cell_type} breast cancer"
                _, _, _ = medrag.answer(
                    question=query, 
                    k=k_, 
                    abm=True, 
                    cell_type=cell_type, 
                    signal=signal, 
                    other_cell_types = ", ".join([c for c in cell_types if c != cell_type]),
                    other_signals = ", ".join([s for s in signals if s != signal]),
                    save_dir=f'abm-rules-MedCPT-k={k_}-full-text-flash/run-{i}',
                    snippets=snippets)
                time.sleep(10)
                break
            break
        

