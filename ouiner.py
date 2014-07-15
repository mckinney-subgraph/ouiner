import csv
import re
import json
import glob

class OuiDb:
    def __init__(self):
        self.entries = []
    def parse_common(self):
        with open('data/oui.txt', 'r') as oui_file:
            for row in oui_file:
                entry_match = re.search(r'.+([0-9A-F]{2}-[0-9A-F]{2}-[0-9A-F]{2})[\s]+\(hex\)[\s]+(.+)$', row)   
                if entry_match:
                    entry = OuiEntry()
                    entry.vendor_prefix = entry_match.group(1).replace("-", ":")
                    entry.vendor_name = entry_match.group(2)
                    device = {
                            'device_name':'Unknown',
                            'device_type':'Other'
                    }
                    entry.devices.append(device)
                    self.entries.append(entry)
    def parse_popular(self):
        files = glob.glob('data/*.sh')
        for f in files:
            with open(f) as oui_file:
                for row in oui_file:
                    device_type_match = re.search(r'^(oui_.+)=\($', row)
                    if device_type_match:
                        device_type = device_type_match.group(1)
                    else:
                        oui_match = re.search(r'^.+([0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2})=\'(.+)\|(.+)\'$', row)
                        if oui_match:
                            vendor_prefix = oui_match.group(1)
                            vendor_name = oui_match.group(2)
                            device_name = oui_match.group(3)
                            entry = self.search_by_vendor_prefix(vendor_prefix)[0]
                            entry.devices[0] = {
                                'device_name': device_name,
                                'device_type': device_type
                            }
                            entry.is_popular = True

    def search_by_vendor_name(self, vendor_name):
        results = [x for x in self.entries if x.vendor_name == vendor_name]
        return results
    
    def search_by_vendor_prefix(self, vendor_prefix):
        results = [x for x in self.entries if x.vendor_prefix == vendor_prefix.upper()]
        return results
    
    def search_by_popular(self):
        results = [x for x in self.entries if x.is_popular]
        return results

    def encode_entry(self, obj):
            if isinstance(obj, OuiEntry):
                return obj.__dict__
            return obj
    
    def dump(self):
        return json.dumps(self.entries, default=self.encode_entry, sort_keys = False, indent = 4)

class OuiEntry:
    def __init__(self):
        self.vendor_prefix = "" 
        self.vendor_name = ""
        self.devices = []
        self.is_popular = False

if __name__ == '__main__':
    ouidb = OuiDb()
    ouidb.parse_common()
    ouidb.parse_popular()
    print(ouidb.dump())
