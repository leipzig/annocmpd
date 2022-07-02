# compound_library
Verify clinical trial stage and patent information for compound library entries

Resources to check:
- PubChem
  - https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/1445993-26-9/
  - https://github.com/mcs07/PubChemPy
  - https://github.com/skearnes/pubchem-utils
  - https://github.com/metamolecular/pubchem-fu
  - bioassayR
  - https://github.com/gorgitko/molminer

There are 8376 compounds in PubChem annotated for clinical trials corresponding to 27502 trials (NCT entries)

- SureChEMBL
  - https://www.surechembl.org/search/
  - https://github.com/chembl/surechembl-data-client
- ChemSpider
  - https://github.com/ropensci/webchem
  - http://www.chemspider.com/
  
  `Consumer Key	xxxxxxxxx`
  `Consumer Secret	xxxxxxxxx`
  
- PharmKGB
  - https://www.pharmgkb.org/
- DrugBank
  - https://www.drugbank.ca/
- Open Phacts
  - https://www.openphacts.org/
- SWEETLEAD
  - https://simtk.org/home/sweetlead
- ClinicalTrials.gov
  - https://clinicaltrials.gov/ct2/results/download_fields?drug=Mivebresib&down_count=10
  - https://github.com/jasonbaik94/clinical_trials
  - https://github.com/ctti-clinicaltrials/aact
  `Hostname: aact-db.ctti-clinicaltrials.org`
  `Port: 5432`
  `Database name: aact`
  `ID/Username: xxxxxxx`
  `Password: xxxxxxxxx`

# Guide to the annotated compound library
```
B - Bad XML - PubChem can't find this CAS Number
N - No trial information
1 - Phase 1
2 - Phase 2
3 - Phase 3
4 - Phase 4
M - Missing annotation (internal)
R - Recruiting
T - Terminated
W - Withdrawn
? - No stage given
```

- Collaborative Drug Discovery
  - http://app.collaborativedrug.com
  - 