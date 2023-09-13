from pprint import pprint
import CloudflareManager
apikey = "96d308eccd656388c9da4b53975f9aef5f3ab"
email = "kfirgoldman12@gmail.com"
pprint(CloudflareManager.ListDomains(email, apikey).ListDomainRecordsData(
    str(CloudflareManager.ListDomains(email, apikey).GetDomainId("tavernxkobold.xyz"))))
