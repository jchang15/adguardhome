from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
import ssl
import requests
import json

## CHANGE HERE ##
# IP address of AdGuard Home
# "http(s)://<adguardHomeIp:<port>"
host = "http://192.168.1.22:80"
# Username
userName = "jc"
# Password
password = "!June@0164"

# Block list
# Taken from Wally3K's Firebog https://firebog.net/
urls = [
    "https://abp.oisd.nl/",
    "https://hblock.molinero.dev/hosts_adblock.txt",
    "https://hblock.molinero.dev/hosts",
    "https://hblock.molinero.dev/hosts_domains.txt",
    "https://raw.githubusercontent.com/kboghdady/youTube_ads_4_pi-hole/master/youtubelist.txt",
    "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts",
    "https://raw.githubusercontent.com/PolishFiltersTeam/KADhosts/master/KADhosts.txt",
    "https://raw.githubusercontent.com/FadeMind/hosts.extras/master/add.Spam/hosts",
    "https://v.firebog.net/hosts/static/w3kbl.txt",
    "https://raw.githubusercontent.com/matomo-org/referrer-spam-blacklist/master/spammers.txt",
    "https://raw.githubusercontent.com/VeleSila/yhosts/master/hosts",
    "https://winhelp2002.mvps.org/hosts.txt",
    "https://v.firebog.net/hosts/neohostsbasic.txt",
    "https://raw.githubusercontent.com/RooneyMcNibNug/pihole-stuff/master/SNAFU.txt",
    "https://paulgb.github.io/BarbBlock/blacklists/hosts-file.txt",
    "https://hostsfile.mine.nu/hosts0.txt",
    "https://v.firebog.net/hosts/BillStearns.txt",
    "https://hostsfile.org/Downloads/hosts.txt",
    "https://www.joewein.net/dl/bl/dom-bl-base.txt",
    "https://v.firebog.net/hosts/Kowabit.txt",
    "https://adblock.mahakala.is",
    "https://v.firebog.net/hosts/AdguardDNS.txt",
    "https://v.firebog.net/hosts/Admiral.txt",
    "https://raw.githubusercontent.com/anudeepND/blacklist/master/adservers.txt",
    "https://s3.amazonaws.com/lists.disconnect.me/simple_ad.txt",
    "https://v.firebog.net/hosts/Easylist.txt",
    "https://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts&showintro=0&mimetype=plaintext",
    "https://raw.githubusercontent.com/FadeMind/hosts.extras/master/UncheckyAds/hosts",
    "https://raw.githubusercontent.com/bigdargon/hostsVN/master/hosts",
    "https://raw.githubusercontent.com/jdlingyu/ad-wars/master/hosts",
    "https://v.firebog.net/hosts/Easyprivacy.txt",
    "https://v.firebog.net/hosts/Prigent-Ads.txt",
    "https://raw.githubusercontent.com/FadeMind/hosts.extras/master/add.2o7Net/hosts",
    "https://hostfiles.frogeye.fr/firstparty-trackers-hosts.txt",
    "https://hostfiles.frogeye.fr/multiparty-trackers-hosts.txt",
    "https://www.github.developerdan.com/hosts/lists/ads-and-tracking-extended.txt",
    "https://raw.githubusercontent.com/Perflyst/PiHoleBlocklist/master/android-tracking.txt",
    "https://gitlab.com/quidsup/notrack-blocklists/raw/master/notrack-blocklist.txt",
    "https://raw.githubusercontent.com/Kees1958/W3C_annual_most_used_survey_blocklist/6b8c2411f22dda68b0b41757aeda10e50717a802/TOP_EU_US_Ads_Trackers_HOST",
    "https://raw.githubusercontent.com/DandelionSprout/adfilt/master/Alternate%20versions%20Anti-Malware%20List/AntiMalwareHosts.txt",
    "https://osint.digitalside.it/Threat-Intel/lists/latestdomains.txt",
    "https://s3.amazonaws.com/lists.disconnect.me/simple_malvertising.txt",
    "https://v.firebog.net/hosts/Prigent-Crypto.txt",
    "https://bitbucket.org/ethanr/dns-blacklists/raw/8575c9f96e5b4a1308f2f12394abd86d0927a4a0/bad_lists/Mandiant_APT1_Report_Appendix_D.txt",
    "https://phishing.army/download/phishing_army_blocklist_extended.txt",
    "https://gitlab.com/quidsup/notrack-blocklists/raw/master/notrack-malware.txt",
    "https://raw.githubusercontent.com/Spam404/lists/master/main-blacklist.txt",
    "https://raw.githubusercontent.com/FadeMind/hosts.extras/master/add.Risk/hosts",
    "https://v.firebog.net/hosts/Prigent-Malware.txt",
    "https://v.firebog.net/hosts/Shalla-mal.txt",
    "https://raw.githubusercontent.com/tg12/pihole-phishtank-list/master/list/phish_domains.txt",
    "https://raw.githubusercontent.com/HorusTeknoloji/TR-PhishingList/master/url-lists.txt",
    "https://zerodot1.gitlab.io/CoinBlockerLists/hosts_browser",
    "https://mirror1.malwaredomains.com/files/justdomains",
    "https://mirror.cedia.org.ec/malwaredomains/immortal_domains.txt",
    "https://www.malwaredomainlist.com/hostslist/hosts.txt",
    "https://urlhaus.abuse.ch/downloads/hostfile/",
    "https://adaway.org/hosts.txt",
    "https://raw.githubusercontent.com/PolishFiltersTeam/KADhosts/master/KADhosts_without_controversies.txt",
    "https://raw.githubusercontent.com/crazy-max/WindowsSpyBlocker/master/data/hosts/spy.txt"
]

############ End Edits #################

# Open TLSv1 Adapter
class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLS)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'}

s = requests.Session()
s.mount(host, MyAdapter())

# Login
login_data = {"name": userName, "password": password}
x = s.post(host + "/control/login", json=login_data, headers=headers)
print(x.text)

# Add URLs to block list
for u in urls:
    filter_data = {'url': u, "name": u, "whitelist": False}
    print(filter_data)
    x = s.post(host + "/control/filtering/add_url", json=filter_data, headers=headers)
    print(x.text)
