race_lookup = {
    "1": "American Indian or Alaska Native",
    "2": "Asian",
    "21": "Asian Indian",
    "22": "Chinese",
    "23": "Filipino",
    "24": "Japanese",
    "25": "Korean",
    "26": "Vietnamese",
    "27": "Other Asian",
    "3": "Black or African American",
    "4": "Native Hawaiian or Other Pacific Islander",
    "41": "Native Hawaiian",
    "42": "Guamanian or Chamorro",
    "43": "Samoan",
    "44": "Other Pacific Islander",
    "5": "White",
}

class Applicant:
    def __init__(self, age, race):
        self.age = age
        self.race = set()
       
        for r in race:
            if r in race_lookup:
                self.race.add(race_lookup[r])
            
    def __repr__(self):
        return f"Applicant({repr(self.age)}, {sorted(list(self.race))})"
    
    def lower_age(self):
        return int(self.age.replace(">", "").replace("<", "").split("-")[0])
    
    def __lt__(self, other):
        return self.lower_age() < other.lower_age() 
    
class Loan:
    def __init__(self, fields):
        if fields["loan_amount"] == "Exempt" or fields["loan_amount"] == "NA":
            self.loan_amount = -1
        else:
            self.loan_amount = float(fields["loan_amount"])
            
        if fields['property_value'] == "Exempt" or fields['property_value'] == "NA":
            self.property_value = -1
        else:
            self.property_value = float(fields['property_value'])
            
        if fields['interest_rate'] == "Exempt" or fields['interest_rate'] == "NA":
            self.interest_rate = -1
        else:
            self.interest_rate = float(fields['interest_rate'])
        
        race_val = []
        for race in fields:
            if race.startswith("applicant_race-") == True and "co" not in race and fields[race] != '':
                for v in range(1, 6):
                    if str(v) in race:
                        race_val.append(fields[f"applicant_race-{v}"])
        self.applicants = [Applicant(fields["applicant_age"], race_val)]
        
        co_race_val = []
        if fields["co-applicant_age"] != "9999":
            for co_app in fields:
                if co_app.startswith("co-applicant_race-") == True and fields[co_app] != '':
                    for x in range(1, 6):
                        if str(x) in co_app:
                            co_race_val.append(fields[f"co-applicant_race-{x}"])
            self.applicants.append(Applicant(fields["co-applicant_age"], co_race_val))
           
    def __str__(self):
        return f"<Loan: {self.interest_rate}% on ${self.property_value} with {len(self.applicants)} applicant(s)>"
        
    def __repr__(self):
        return f"<Loan: {self.interest_rate}% on ${self.property_value} with {len(self.applicants)} applicant(s)>"
    
    def yearly_amounts(self, yearly_payment):
        result = []
        amt = self.loan_amount
        assert self.interest_rate > 0 and amt > 0
        
        while amt > 0:
            yield amt
            amt = amt + ((self.interest_rate / 100) * amt) - yearly_payment
            
class Bank:
    def __init__(self, title):
        import json
        with open("banks.json") as f:
            banks = json.load(f)
            
            for values in banks:
                if values['name'] == title:
                    lei_val = values['lei']
            self.lei = lei_val
            
        from io import TextIOWrapper
        from zipfile import ZipFile
        import csv
        
        loans = []
        with ZipFile('wi.zip') as zf:
            with zf.open('wi.csv', "r") as f:
                tio = TextIOWrapper(f)
                reader = csv.DictReader(tio)
                for row in reader:
                    if row['lei'] == self.lei:
                        loans.append(Loan(row))
        self.loaninfo = loans
        
    def __getitem__(self, lookup):
        return self.loaninfo[lookup]
    
    def __len__(self):
        return len(self.loaninfo)
