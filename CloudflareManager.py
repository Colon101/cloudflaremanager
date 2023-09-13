import requests


class ListDomains:
    def __init__(self, email: str, apikey: str):
        AccountsURL = "https://api.cloudflare.com/client/v4/accounts"
        self.email = email
        self.apikey = apikey
        self.headers = {
            "Content-Type": "application/json",
            "X-Auth-Email": f"{email}",
            "X-Auth-Key": f"{apikey}"
        }

        response = requests.request("GET", AccountsURL, headers=self.headers)
        data = response.json()
        if data["success"] == True:
            self.accountid = data["result"][0]["id"]
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


class ViewDomainRecords:
    def __init__(self, Email: str, ApiKey: str):
        AccountsURL = "https://api.cloudflare.com/client/v4/accounts"
        self.Email = Email
        self.ApiKey = ApiKey
        self.Headers = {
            "Content-Type": "application/json",
            "X-Auth-Email": f"{self.Email}",
            "X-Auth-Key": f"{self.ApiKey}"
        }
        response = requests.request("GET", AccountsURL, headers=self.Headers)
        data = response.json()
        if data["success"] == True:
            self.accountid = data["result"][0]["id"]
        else:
            raise Exception("Errors: "+str(data['errors'][0]))

    def ListDomainRecordsData(self, DomainId):
        ListDomainURL = f"https://api.cloudflare.com/client/v4/zones/{DomainId}/dns_records"
        response = requests.request(
            "GET", url=ListDomainURL, headers=self.Headers)
        return response.json()["result"]
