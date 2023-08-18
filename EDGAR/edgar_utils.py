import re
import netaddr
from bisect import bisect
import pandas as pd

ips_df = pd.read_csv("ip2location.csv")

def lookup_region(ip_address):
    global ips_df
    fixed_ip = re.sub(r'[a-zA-Z]', '0', ip_address)
    int_ip = int(netaddr.IPAddress(fixed_ip))
    idx = bisect(ips_df['low'], int_ip)
    return ips_df.iloc[idx - 1]['region']

class Filing:
    def __init__(self, html):
        self.dates = re.findall(r"19[0-9][0-9]-\d{2}-\d{2}|20[0-9][0-9]-\d{2}-\d{2}", html)
        self.sic = 0
        self.addresses = []
        
        try:
            val = int(re.search(r"SIC=(\d+)", html).group(1))
            self.sic = val
        except:
            self.sic = None
        
        for addr_html in re.findall(r'<div class="mailer">([\s\S]+?)</div>', html):
            lines = []
            for line in re.findall(r'<span class="mailerAddress">([\s\S]+?)</span>', addr_html):
                lines.append(line.strip())
            if lines:
                self.addresses.append("\n".join(lines))
                
    def state(self):
        for address in self.addresses:
            states = re.search(r"([A-Z]{2}) \d{5}", address)
            if states is not None: #(!= None)
                return states.group(1)
        return None
    
                     