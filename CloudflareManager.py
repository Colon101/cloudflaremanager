from typing import Any
import requests


class CloudflareManager:
    def __init__(self, email: str, apikey: str) -> None:

        self.__email = email
        self.__apikey = apikey
        self.headers = {
            "Content-Type": "application/json",
            "X-Auth-Email": f"{self.__email}",
            "X-Auth-Key": f"{self.__apikey}"
        }
        self.accountid = self.__GetAccountId()

    def __GetAccountId(self) -> str:
        AccountsURL = "https://api.cloudflare.com/client/v4/accounts"
        response = requests.request("GET", AccountsURL, headers=self.headers)
        data = response.json()
        if data["success"] == True:
            return data["result"][0]["id"]
        else:
            raise Exception("Errors: "+str(data['errors'][0]))

    def GetDomainData(self):
        DomainsURL = f"https://api.cloudflare.com/client/v4/zones"
        response = requests.request("GET", DomainsURL, headers=self.headers)
        data = response.json()
        domains = []
        ids = []
        for i in range(len(data["result"])):
            domains.append(data["result"][i]["name"])
            ids.append(data["result"][i]["id"])
        self.DomainInfo = zip(domains, ids)
        self.DomainInfo = dict(self.DomainInfo)
        return self.DomainInfo

    def GetDomainId(self, Domain: str):
        OwnedDomains = self.GetDomainData()
        if Domain in OwnedDomains.keys():
            return OwnedDomains[Domain]
        else:
            raise Exception("NoOwnershipError")

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.headers

    class DomainManagement():
        def __init__(self, DomainId: str, headers: dict) -> None:
            """call str(CloudFlareManager) to get headers"""
            self.__DomainId = DomainId
            self.headers = headers

        def ListDomainRecordsData(self) -> dict:
            ListDomainURL = f"https://api.cloudflare.com/client/v4/zones/{self.__DomainId}/dns_records"
            response = requests.request(
                "GET", url=ListDomainURL, headers=self.headers)
            name = []
            id = []
            content = []
            recordtype = []
            data = response.json()["result"]
            for i in range(len(data)):
                name.append(data[i]["name"])
                id.append(data[i]["id"])
                recordtype.append(data[i]["type"])
                content.append(data[i]["content"])
            DomainRecordsData = {}
            for i in range(len(data)):
                DomainRecordsData[f"{name[i]}"] = {"id": id[i],
                                                   "type": recordtype[i], "content": content[i]}
            return DomainRecordsData

        def GetRecordId(self, RecordName: str) -> str:
            Records = self.ListDomainRecordsData(DomainId=self.__DomainId)
            return Records[RecordName]["id"]

        def GetRecordData(self, RecordId: str) -> dict:
            Records = self.ListDomainRecordsData(DomainId=self.__DomainId)
            for key, value in Records.items():
                if 'id' in value and value['id'] == RecordId:
                    result = value.copy()
                    result['name'] = key
                    result.pop('id', None)
                    return result
            raise Exception("No Such Record Found")
