import boto3
import json
import decimal
import sys


dynamodb = boto3.resource('dynamodb') #, region_name='us-west-2', endpoint_url="http://localhost:8000")

table = dynamodb.Table('pubchem_ct_annos')

# >>> one['Annotations']["Annotation"][1]
# {'SourceName': 'ClinicalTrials.gov', 'SourceID': 'cid5353613', 'Name': 'Eicosapentaenoic acid ethyl ester', 'URL': 'https://clinicaltrials.gov/', 'LinkToPubChemBy': {'CID': [5353613]}, 'Data': [{'TOCHeading': 'Clinical Trials', 'Name': 'Clinical Trials', 'Value': {'Table': {'ColumnName': ['Record ID', 'Title', 'Status', 'Phase'], 'Row': [{'Cell': [{'StringValue': 'NCT00231738', 'URL': 'https://clinicaltrials.gov/show/NCT00231738'}, {'StringValue': 'Protective Effect of EPA on Cardiovascular Events'}, {'StringValue': 'Completed'}, {'StringValue': '4'}]}, {'Cell': [{'StringValue': 'NCT00839449', 'URL': 'https://clinicaltrials.gov/show/NCT00839449'}, {'StringValue': '<a class="pubchem-internal-link CID-446284" href="https://pubchem.ncbi.nlm.nih.gov/compound/Eicosapentaenoic%20Acid">Eicosapentaenoic Acid</a> Cerebral Vasospasm Therapy Study'}, {'StringValue': 'Completed'}, {'StringValue': '4'}]}], 'ExternalTableName': 'clinicaltrials', 'ExternalTableNumRows': 2}}}]}
# >>> one['Annotations']["Annotation"][1]['SourceID']
# 'cid5353613'


def loadClinfile(filename):
    with open(filename) as json_file:
        print("opening"+sys.argv[1]+"\n")
        annos = json.load(json_file, parse_float = decimal.Decimal)['Annotations']["Annotation"]
        for anno in annos:
            print("Adding anno:"+anno['SourceID'])
    
            table.put_item(
               Item=anno
            )
            
            cid=table.get_item(Key={'SourceID':anno['SourceID']})
            if 'Item' in cid:
                if 'Data' in cid['Item']:
                    if 'Table' in cid['Item']['Data'][0]['Value']:
                        if 'Row' in cid['Item']['Data'][0]['Value']['Table']:
                            trials = {}
                            for cell in cid['Item']['Data'][0]['Value']['Table']['Row']:
                                if cell['Cell'][2]['StringValue'] in ['Terminated','Recruiting','Withdrawn']:
                                    trials[cell['Cell'][2]['StringValue'][0:1]]=trials.get(cell['Cell'][2]['StringValue'][0:1],0)+1
                                else:
                                    if 'StringValue' in cell['Cell'][3]:
                                        stage=str(cell['Cell'][3]['StringValue'])
                                    else:
                                        stage='?'
                                    trials[stage]=trials.get(stage,0)+1
                            trialSummary = []
                            for k,v in sorted(trials.items()):
                                trialSummary += ["{}:{}".format(k,v)]
                            cid['Item']['Data'][0]['Value']['Table']['trialSummary']=trialSummary
                            print(trialSummary)
                            table.put_item(
                               Item=cid['Item']
                            )
                        else:
                            print("{0} has a Table but no Row".format(anno['SourceID']))
                    else:
                        print("{0} has no Table".format(anno['SourceID']))
                else:
                    print("{0} has no Data".format(anno['SourceID']))
            else:
                print("{0} has no Item".format(anno['SourceID']))

def printEntry(cid):
    cid=table.get_item(Key={'SourceID':cid})
    print(cid)

def getEntry(cid):
    cid=table.get_item(Key={'SourceID':cid})
    return(cid)

if __name__== "__main__":
  loadClinfile(sys.argv[1])
#cid=table.get_item(Key={'SourceID':'cid5353613'})
#the number of clinical trials
#len(cid['Item']['Data'][0]['Value']['Table']['Row'])

# {'Cell': [
#     {'StringValue': 'NCT02886793', 'URL': 'https://clinicaltrials.gov/show/NCT02886793'}, 
#     {'StringValue': 'Cell Proliferation in Pulmonary Hypertension. FDG-PET Comparison Between Patients and Healthy Subjects'}, 
#     {'StringValue': 'Active, not recruiting'}, 
#     {'StringValue': '2'}]}

# {'Item': {'LinkToPubChemBy': {'CID': [Decimal('6014')]}, 'SourceID': 'cid6014', 'SourceName': 'ClinicalTrials.gov', 'Data': 
#     [{'TOCHeading': 'Clinical Trials', 'Value': {
#         'Table': {'ColumnName': ['Record ID', 'Title', 'Status', 'Phase'], 'ExternalTableName': 'clinicaltrials', 
#         'Row': [
#             {'Cell': [{'StringValue': 'NCT00541671', 'URL': 'https://clinicaltrials.gov/show/NCT00541671'}, {'StringValue': 'Prevention of Narcotic-Induced Nausea'}, {'StringValue': 'Terminated'}, {}]}, 
#             {'Cell': [{'StringValue': 'NCT00947063', 'URL': 'https://clinicaltrials.gov/show/NCT00947063'}, {'StringValue': 'To Demonstrate the Relative Bioavailability Study of <a class="pubchem-internal-link CID-6014" href="https://pubchem.ncbi.nlm.nih.gov/compound/Promethazine%20HCl">Promethazine HCl</a> 50 mg Tablets Under Fasting Conditions'}, {'StringValue': 'Completed'}, {'StringValue': '1'}]}, 
#             {'Cell': [{'StringValue': 'NCT01100645', 'URL': 'https://clinicaltrials.gov/show/NCT01100645'}, {'StringValue': 'Efficacy and Safety of the Herbal Medicine <a class="pubchem-internal-link multiple-CIDs" href="https://pubchem.ncbi.nlm.nih.gov/compound/Sominex">Sominex</a> ® (Passiflora Incarnata L., Valeriana Officinalis L. and Crataegus Oxyacantha L.), Manufactured by the Laboratory EMS S / A in Patients With Psychophysiological Insomnia'}, {'StringValue': 'Unknown status'}, {'StringValue': '3'}]}, 
#             {'Cell': [{'StringValue': 'NCT02465866', 'URL': 'https://clinicaltrials.gov/show/NCT02465866'}, {'StringValue': 'A Four-Period, Four-Treatment, Four-Way Relative Bioavailability Study of CL-108 Under Fed and Fasted Conditions'}, {'StringValue': 'Completed'}, {'StringValue': '1'}]}, 
#             {'Cell': [{'StringValue': 'NCT02473042', 'URL': 'https://clinicaltrials.gov/show/NCT02473042'}, {'StringValue': 'Intraoperative Acupoint Stimulation to Prevent Post-Operative Nausea and Vomiting (PONV)'}, {'StringValue': 'Recruiting'}, {}]}],
            
#             'ExternalTableNumRows': Decimal('5')}}, 'Name': 'Clinical Trials'}], 'URL': 'https://clinicaltrials.gov/', 'Name': 'Promethazine hydrochloride'}, 
#             'ResponseMetadata': {'RequestId': 'CTMSBUN4B65EG3J8NM7GAAVCNRVV4KQNSO5AEMVJF66Q9ASUAAJG', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'Server', 'date': 'Thu, 14 Feb 2019 18:19:52 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '2396', 'connection': 'keep-alive', 'x-amzn-requestid': 'CTMSBUN4B65EG3J8NM7GAAVCNRVV4KQNSO5AEMVJF66Q9ASUAAJG', 'x-amz-crc32': '1235196823'}, 'RetryAttempts': 0}}

# {'Item': {'LinkToPubChemBy': {'CID': [Decimal('53486260')]}, 'SourceID': 'cid53486260', 'SourceName': 'ClinicalTrials.gov', 'Data': 
#     [{'TOCHeading': 'Clinical Trials', 'Value': {'Table': {'ColumnName': ['Record ID', 'Title', 'Status', 'Phase'], 'ExternalTableName': 'clinicaltrials', 
#     'Row': [{'Cell': [{'StringValue': 'NCT00004786', 'URL': 'https://clinicaltrials.gov/show/NCT00004786'}, {'StringValue': 'Phase III Randomized, Double-Blind, Placebo-Controlled Study of Oral <a class="pubchem-internal-link CID-6435378" href="https://pubchem.ncbi.nlm.nih.gov/compound/Iloprost">Iloprost</a> for Raynaud\'s Phenomenon Secondary to Systemic Sclerosis'}, {'StringValue': 'Completed'}, {'StringValue': '3'}]}, 
#     {'Cell': [{'StringValue': 'NCT00084409', 'URL': 'https://clinicaltrials.gov/show/NCT00084409'}, {'StringValue': '<a class="pubchem-internal-link CID-6435378" href="https://pubchem.ncbi.nlm.nih.gov/compound/Iloprost">Iloprost</a> in Preventing Lung Cancer in Patients at High Risk for This Disease'}, {'StringValue': 'Completed'}, {'StringValue': '2'}]},
#     {'Cell': [{'StringValue': 'NCT00086463', 'URL': 'https://clinicaltrials.gov/show/NCT00086463'}, {'StringValue': 'Trial of <a class="pubchem-internal-link CID-6435378" href="https://pubchem.ncbi.nlm.nih.gov/compound/Iloprost">Iloprost</a> Inhaled Solution as Add-On Therapy With <a class="pubchem-internal-link CID-104865" href="https://pubchem.ncbi.nlm.nih.gov/compound/Bosentan">Bosentan</a> in Subjects With Pulmonary Arterial Hypertension (PAH)'}, {'StringValue': 'Completed'}, {'StringValue': '2'}]}, 
#     {'Cell': [{'StringValue': 'NCT00216931', 'URL': 'https://clinicaltrials.gov/show/NCT00216931'}, {'StringValue': 'Treatment of Elevated Arterial Pulmonary Pressure With Inhaled <a class="pubchem-internal-link CID-6435378" href="https://pubchem.ncbi.nlm.nih.gov/compound/Iloprost">Iloprost</a>'}, {'StringValue': 'Withdrawn'}, {}]}, 
#     {'Cell': [{'StringValue': 'NCT00250640', 'URL': 'https://clinicaltrials.gov/show/NCT00250640'}, {'StringValue': 'Observation of Patients With Primary Pulmonary Hypertension Receiving Prescribed <a class="pubchem-internal-link multiple-CIDs" href="https://pubchem.ncbi.nlm.nih.gov/compound/Ventavis">Ventavis</a> Inhalation Therapy Regarding Safety and Efficacy for up to 4 Years'}, {'StringValue': 'Completed'}, {}]}], 
#     'ExternalTableNumRows': Decimal('38')}}, 'Name': 'Clinical Trials'}], 'URL': 'https://clinicaltrials.gov/', 'Name': 'Iloprost'}, 'ResponseMetadata': {'RequestId': 'QFDF8D3GS34MV0F3PHKK9ND0CVVV4KQNSO5AEMVJF66Q9ASUAAJG', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'Server', 'date': 'Thu, 14 Feb 2019 18:34:45 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '2809', 'connection': 'keep-alive', 'x-amzn-requestid': 'QFDF8D3GS34MV0F3PHKK9ND0CVVV4KQNSO5AEMVJF66Q9ASUAAJG', 'x-amz-crc32': '3045644785'}, 'RetryAttempts': 0}}


#cid69211190