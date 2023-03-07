import csv
from fileinput import filename
from operator import truediv
import pandas as pd
from datetime import datetime


#list to keep track of pairs made
pairs = []
# match_threshold = 120

# filename = 'typeform_responses.csv'

file = open(filename, 'r', encoding="utf8")
datareader = csv.reader(file)
dr = list(datareader)

#personality
def get_personality_averages(arr):
        result = []
        for i in range(24, 54, 6):
            sum = int(arr[i]) + int(arr[i+1]) + int(arr[i+2]) + int(arr[i+3]) + int(arr[i+4]) + int(arr[i+5])
            result.append(sum / 6)
        return result

def score_personality_match(person1, person2): 
    personality_score = 0
    for i in range(5):
        if int(person1[i]) in range(int(person2[i])-1, int(person2[i])+1):
            personality_score += 20         
    return personality_score

#age
def get_age(birth_date):
    # Convert the birth date string to a datetime object
    clean_birth_date = birth_date[:10]
    birth_datetime = datetime.strptime(clean_birth_date, "%Y-%m-%d")
    
    # Get the current date and time
    now = datetime.now()
    
    # Calculate the difference between the two dates
    age_in_seconds = (now - birth_datetime).total_seconds()
    
    # Convert the age from seconds to years
    age_in_years = int(age_in_seconds / 31536000)
    return age_in_years

def is_in_age_range(person1, person2): 
    # checks if person2 is within the prefered age range of person1
    
    person1_age = get_age(person1[7])
    person2_age = get_age(person2[7])
    
    upper_age_limit = person1_age + int(person1[76])
    lower_age_limit = person1_age - int(person1[77])
    
    return lower_age_limit <= person2_age <= upper_age_limit

#religion
def calc_religiousity(person):
    religiousity_score = int(person[54])*6 + int(person[55])*2.6 + int(person[56])*2.6 + int(person[57])*1.3 + int(person[58])*3 + int(person[59])
    return int(religiousity_score)

def calc_religiousity_match(person1, person2):
    match = 0
    if calc_religiousity(person1) == calc_religiousity(person2):
        match = 100
    elif abs(calc_religiousity(person1) - calc_religiousity(person2)) < 6:
        match = 95
    elif abs(calc_religiousity(person1) - calc_religiousity(person2)) < 11:
        match = 90
    elif abs(calc_religiousity(person1) - calc_religiousity(person2)) < 16:
        match = 85
    elif abs(calc_religiousity(person1) - calc_religiousity(person2)) < 21:
        match = 80
    return int(match)

def is_same_sect(person1, person2):
    if person1[16] == person2[16]:
        return True

#ethnicity
def convert_nationality_to_ethnicity(nationality):
    if nationality == "Angola" or nationality == "Benin" or nationality == "Botswana" or nationality == "Burkina" or nationality == "Burundi" or nationality == "Cameroon" or nationality == "Cape Verde" or nationality == "Central African Rep" or nationality == "Chad" or nationality == "Comoros" or nationality == "Congo" or nationality == "Congo {Democratic Rep}" or nationality == "Djibouti" or nationality == "Equatorial Guinea" or nationality == "Eritrea" or nationality == "Ethiopia" or nationality == "Gabon" or nationality == "Gambia" or nationality == "Ghana" or nationality == "Guinea" or nationality == "Guinea-Bissau" or nationality == "Ivory Coast" or nationality == "Kenya" or nationality == "Liberia" or nationality == "Lesotho" or nationality == "Madagascar" or nationality == "Malawi" or nationality == "Mali" or nationality == "Mauritania" or nationality == "Mauritius" or nationality == "Mozambique" or nationality == "Namibia" or nationality == "Niger" or nationality == "nigeria" or nationality == "Rwanda" or nationality == "Sao Tome & Principe" or nationality == "Senegal" or nationality == "Seychelles" or nationality == "Sierra Leone" or nationality == "Somalia" or nationality == "South Africa" or nationality == "South Sudan" or nationality == "Sudan" or nationality == "Swaziland" or nationality == "Tanzania" or nationality == "Togo" or nationality == "Uganda" or nationality == "Zambia" or nationality == "Zimbabwe":
        return "African"
    if nationality == "Brunei" or nationality == "Cambodia" or nationality == "China" or nationality == "East Timor" or nationality == "Indonesia" or nationality == "Japan" or nationality == "Korea North" or nationality == "Korea South" or nationality == "Laos" or nationality == "Malaysia" or nationality == "Mongolia" or nationality == "Myanmar, {Burma}" or nationality == "Philippines" or nationality == "Singapore" or nationality == "Taiwan" or nationality == "Thailand" or nationality == "Vietnam" or nationality == "Bhutan":
        return "Asian"    
    if nationality == "Bangladesh" or nationality == "India" or nationality == "Pakistan" or nationality == "Kashmir" or nationality == "Sri Lanka" or nationality == "Guyana" or nationality == "Nepal":
        return "Desi"
    if nationality == "Albania" or nationality == "Belarus" or nationality == "Bosnia Herzegovina" or nationality == "Bulgaria" or nationality == "Croatia" or nationality == "Czech Republic" or nationality == "Estonia" or nationality == "Serbia" or nationality == "Slovakia" or nationality == "Slovenia" or nationality == "Russian Federation" or nationality == "Romania" or nationality == "Ukraine" or nationality == "Latvia" or nationality == "Lithuania" or nationality == "Kosovo" or nationality == "Macedonia" or nationality == "Montenegro" or nationality == "Moldova" or nationality == "Malta" or nationality == "Georgia" or nationality == "Greece" or nationality == "Cyprus":
        return "Eastern European"
    if nationality == "Argentina" or nationality == "Belize" or nationality == "Bolivia" or nationality == "Brazil" or nationality == "Chile" or nationality == "Colombia" or nationality == "Costa Rica" or nationality == "Cuba" or nationality == "Dominican Republic" or nationality == "Ecuador" or nationality == "El Salvador" or nationality == "Guatemala" or nationality == "Honduras" or nationality == "Nicaragua" or nationality == "Venezuela" or nationality == "Peru" or nationality == "Paraguay" or nationality == "Uruguay" or nationality == "Panama" or nationality == "Mexico" or nationality == "Suriname":
        return "Hispanic/Latino"
    if nationality == "Bahrain" or nationality == "United Arab Emirates" or nationality == "Yemen" or nationality == "Saudi Arabia" or nationality == "Iraq" or nationality == "Qatar" or nationality == "Oman" or nationality == "Kuwait" or nationality == "Armenia" or nationality == "Turkey":
        return "Middle Eastern"
    if nationality == "Afghanistan" or nationality == "Iran" or nationality == "Tajikistan":
        return "Persian"
    if nationality == "Australia" or nationality == "Austria" or nationality == "Belgium" or nationality == "Canada" or nationality == "Denmark" or nationality == "Germany" or nationality == "France" or nationality == "United Kingdom" or nationality == "United States" or nationality == "Finland" or nationality == "Iceland" or nationality == "Poland" or nationality == "Hungary" or nationality == "Ireland {Republic}" or nationality == "Italy" or nationality == "Andorra" or nationality == "Liechtenstein" or nationality == "Luxembourg" or nationality == "Monaco" or nationality == "Netherlands" or nationality == "New Zealand" or nationality == "Norway" or nationality == "Vatican City" or nationality == "Sweden" or nationality == "Switzerland" or nationality == "Spain" or nationality == "San Marino" or nationality == "Portugal":
        return "White"
    if nationality == "Algeria" or nationality == "Egypt" or nationality == "Libya" or nationality == "Tunisia" or nationality == "Morocco":
        return "North African"
    if nationality == "Jordan" or nationality == "Lebanon" or nationality == "Syria" or nationality == "Palestine":  
        return "Shamy"
    if nationality == "Antigua & Deps" or nationality == "Bahamas" or nationality == "Barbados" or nationality == "Dominica" or nationality == "Grenada" or nationality == "St Kitts & Nevis" or nationality == "St Lucia" or nationality == "Saint Vincent & the Grenadines" or nationality == "Trinidad & Tobago" or nationality == "Jamaica" or nationality == "Haiti" or nationality == "Fiji" or nationality == "Micronesia" or nationality == "Palau" or nationality == "Nauru" or nationality == "Samoa" or nationality == "Solomon Islands" or nationality == "Tonga" or nationality == "Tuvalu" or nationality == "Vanuatu" or nationality == "Kiribati" or nationality == "Marshall Islands" or nationality == "Papua New Guinea" or nationality == "Azerbaijan" or nationality == "Kazakhstan" or nationality == "Kyrgyzstan" or nationality == "Uzbekistan" or nationality == "Turkmenistan":
        return "*Everything, just make them nice *"

def get_ethnicity_preference(person1):
    ethnicities = []
    if person1[88]:
        ethnicities.append("African")
    if person1[89]:
        ethnicities.append("African American")
    if person1[90]:
        ethnicities.append("Asian")    
    if person1[91]:
        ethnicities.append("Desi")    
    if person1[92]:
        ethnicities.append("Eastern European")   
    if person1[93]:
        ethnicities.append("Hispanic/Latino")    
    if person1[94]:    
        ethnicities.append("Middle Eastern")
    if person1[95]:    
        ethnicities.append("North African")
    if person1[96]:    
        ethnicities.append("Persian")
    if person1[97]:    
        ethnicities.append("Shamy")
    if person1[98]:    
        ethnicities.append("White")
    if person1[99]:
        if "African" not in ethnicities:
            ethnicities.append("African")
        if "African American" not in ethnicities:
            ethnicities.append("African American")
        if "Asian" not in ethnicities:
            ethnicities.append("Asian")
        if "Desi" not in ethnicities:
            ethnicities.append("Desi")
        if "Eastern European" not in ethnicities:
            ethnicities.append("Eastern European")
        if "Hispanic/Latino" not in ethnicities:
            ethnicities.append("Hispanic/Latino")
        if "Middle Eastern" not in ethnicities:
            ethnicities.append("Middle Eastern")
        if "North African" not in ethnicities:
            ethnicities.append("North African")
        if "Persian" not in ethnicities:
            ethnicities.append("Persian")
        if "Shamy" not in ethnicities:
            ethnicities.append("Shamy")
        if "White" not in ethnicities:
            ethnicities.append("White")
        if "*Everything, just make them nice *" not in ethnicities:
            ethnicities.append("*Everything, just make them nice *")
    return ethnicities

def is_valid_ethnicity(person1, person2):
    if ( convert_nationality_to_ethnicity(person2[13]) or convert_nationality_to_ethnicity(person2[14]) or convert_nationality_to_ethnicity(person2[15]) in get_ethnicity_preference(person1)) and convert_nationality_to_ethnicity(person1[13]) or convert_nationality_to_ethnicity(person1[14]) or convert_nationality_to_ethnicity(person1[15]) in get_ethnicity_preference(person2):
        return True

def is_same_ethnicity(person1, person2):
    # checks if there is ANY ethnicity match between two people 
    if person1[13] == person2[13]: # full matches full
        return True
    if person1[13] == person2[14]: # full matches dad
        return True
    if person1[13] == person2[15]: # full matches mom
        return True
    if person1[14] == person2[13]: # dad's side matches full
        return True
    if person1[14] == person2[14]: # dad's side matches dad's side
        return True
    if person1[14] == person2[15]: # dad's side matches mom's side
        return True
    if person1[15] == person2[13]: # mom's side matches full
        return True
    if person1[15] == person2[14]: # mom's side matches dad's side
        return True
    if person1[15] == person2[15]: # mom's side matches mom's side
        return True
    return False

#location
def convert_states_to_regions(state):
    if state == "California" or state == "Oregon" or state == "Washington":
        return "Pacific Coastal"
    if state == "Nevada" or state == "Utah" or state == "Colorado" or state == "Idaho" or state == "Wyoming" or state == "Montana":
        return "Rocky Mountains"
    if state == "Ohio" or state == "Michigan" or state == "Indiana" or state == "Illinois" or state == "Wisconson" or state == "Minnesota" or state == "Iowa" or state == "Missouri" or state == "North Dakota" or state == "South Dakota" or state == "Nebraska" or state == "Kansas":
        return "Midwest"
    if state == "Arizona" or state == "New Mexico" or state == "Texas" or state == "Oklahoma":
        return "Southwest"
    if state == "Arkansas" or state == "Louisiana" or state == "Alabama" or state == "Georgia" or state == "Florida" or state == "Mississippi" or state == "Kentucky" or state == "Tennessee" or state == "North Carolina" or state == "South Carolina" or state == "Virginia" or state == "West Virginia":
        return "Southeast"
    if state == "New York" or state == "Pennsylvania" or state == "Delware" or state == "New Jersey" or state == "Maryland":
        return "Mid-Atlantic"
    if state == "Maine" or state == "New Hampshire" or state == "Vermont" or state == "Massachusets" or state == "Rhode Island" or state == "Conneticut":
        return "New England"

def get_region_preference(person1):
    regions = []
    if person1[100]:
        if person1[101]:
            regions.append(person1[101])
        if person1[102]:
            regions.append(person1[102])
        if person1[103]:
            regions.append(person1[103])
        if person1[104]:
            regions.append(person1[104])
        if person1[105]:
            regions.append(person1[105])
        if person1[106]:
            regions.append(person1[107])
        if person1[107]:
            regions.append(person1[107])
    return regions

def is_valid_location(person1, person2):
    person1_region = convert_states_to_regions(person1[19])
    person2_region = convert_states_to_regions(person2[19])
    person1_preference = get_region_preference(person1)
    person2_preference = get_region_preference(person2)
    if person2_region in person1_preference and person1_region in person2_preference:
        return True

#other preferences
def is_student_preference(person1, person2):
    if person1[79] == "1" and person2[79] == "1":
        return True
    elif person1[79] == "1" and person2[79] == "0":
        if "student" not in person1[10]:
            return True
    elif person1[79] == "0" and person2[79] == "1":
        if "student" not in person2[10]:
            return True
    elif person1[79] == "0" and person2[79] == "0":
        if "student" not in person2[10] and "student" not in person1[10]:
            return True    

def is_sah_preference(person1, person2):
    if person1[111] == person2[113]:
        return True

def is_hijab_preference(person1, person2):
    if (person1[112] == "5" or person1[112] == "4" or person1[112] == "3") and (person2[114] == "5" or person2[114] == "4" or person2[114] == "3"):
        return True
    elif (person1[112] == "2" or person1[112] == "1") and (person2[114] == "2" or person2[114] == "1"):
        return True

male = []
female = []
for person in dr:
    if person[6] == "Male":
        male.append(person)
    elif person[6] == "Female":
        female.append(person)

filtered_pairs = []
def filter_dealbreakers(person1, person2, match_score):
    if is_in_age_range(person1, person2) and is_in_age_range(person2, person1):
        if is_same_sect(person1, person2):
            if is_valid_location(person1, person2):
                if person1[19] == person2[19]:
                    match_score = match_score + 30
                if is_student_preference(person1, person2):
                    if is_sah_preference(person1, person2):
                        if is_hijab_preference(person1, person2):
                            if calc_religiousity_match(person1, person2) > 79:
                                if person1[86]: #has to be same ethnicity
                                    if is_same_ethnicity(person1, person2):
                                        filtered_pairs.append([person1, person2, match_score])
                                else:
                                    if is_valid_ethnicity(person1, person2) and is_valid_ethnicity(person2, person1):
                                        if is_same_ethnicity(person1, person2):
                                            match_score = match_score + 10
                                        filtered_pairs.append([person1, person2, match_score])


for m in male:
    for f in female:
        match_score = 0
        filter_dealbreakers(m, f, match_score)

for pair in filtered_pairs:
    man = pair[0]
    woman = pair[1]
    score = pair[2]
    score = score + score_personality_match(get_personality_averages(man), get_personality_averages(woman)) + calc_religiousity_match(man, woman)
    print(pair)
    print(score)
  
    
