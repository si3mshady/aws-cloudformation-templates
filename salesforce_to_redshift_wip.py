
from simple_salesforce import Salesforce
from datetime import datetime
import json, requests


with open('creds.json') as credentials:
    login_creds = json.loads(credentials.read())
   
   
class BusinessIntelligence(Salesforce): 
    def __init__(self, account_id: str = None, creds: dict = login_creds ):
        self.login_creds = login_creds
        self.sf =  Salesforce(**self.login_creds)
        self.sf_instance = self.sf.sf_instance
        self.session_id = self.sf.session_id
        self.accounts = self.query_all_accounts()
        self.security_token = self.login_creds.get('security_token')

    
    def query_all_accounts(self: list):
        query = 'SELECT Id, Name FROM Account'
        return self.sf.bulk.Account.query_all(query)
  

    def get_account_records(self, account_id: str ):  #add fields param later 

        fields = ["Account_ID__c","Industry","Application_Status__c", "OwnerId", "Name"]
        
        headers = {'Authorization': f'Bearer {self.session_id}'}

        querySring = ",".join(fields)

        url = f"https://{self.sf_instance}/services/data/v52.0/sobjects/Account/{account_id}?fields={querySring}"

        resp = requests.get(url=url,headers=headers).json()
        print(resp)

    
    def fetch_salesforce_data(self):
        for account in self.accounts:
            self.get_account_records(account.get('Id'))



bi = BusinessIntelligence()
bi.fetch_salesforce_data()
