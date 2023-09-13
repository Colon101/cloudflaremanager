import requests


class ListDomains:
    def __init__(self, apikey, email):
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


if __name__ == "__main__":
    email = input("enter email: ")
    apikey = input("enter api key: ")
    e = ListDomains(apikey, email)
    print(str(e.GetDomainData()))
