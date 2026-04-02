"""
NCO 2015 Occupation Code Mapping for India Job Market Visualizer
National Classification of Occupations - 2015
Directorate General of Employment, Ministry of Labour & Employment, India

Key occupation categories (1-digit NCO):
1 - Legislators, Senior Officials and Managers
2 - Professionals
3 - Technicians and Associate Professionals
4 - Clerical Support Workers
5 - Service and Sales Workers
6 - Agricultural and Fishery Workers
7 - Craft and Related Trades Workers
8 - Plant and Machine Operators and Assemblers
9 - Elementary Occupations
0 - Armed Forces

This is a simplified mapping focusing on common occupations in PLFS data.
For complete NCO 2015, refer to: https://dge.gov.in/dge/hi/nco-2015
"""

NCO_MAPPING = {
    # 1 - Legislators, Senior Officials and Managers
    "111": "Legislators and Senior Officials",
    "112": "Managing Directors and Chief Executives",
    "121": "Business Services and Administration Managers",
    "122": "Sales, Marketing and Development Managers",
    "131": "Production and Operations Managers",
    "132": "Supply Chain, Logistics and Transport Managers",
    "133": "Information and Communications Technology Services Managers",
    "134": "Professional Services Managers",
    "141": "Finance Managers",
    "142": "Human Resources Managers",
    "143": "Policy and Planning Managers",
    "149": "Other Managers",
    # 2 - Professionals
    "211": "Physicists, Chemists and Related Professionals",
    "212": "Mathematicians, Statisticians and Actuaries",
    "213": "Life Science Professionals",
    "214": "Engineering Professionals",
    "215": "Electrical Engineers",
    "216": "Electronics Engineers",
    "217": "Architects, Planners, Surveyors and Designers",
    "218": "Medical Doctors",
    "221": "University and Higher Education Teachers",
    "222": "Secondary Education Teachers",
    "223": "Primary and Pre-Primary Education Teachers",
    "224": "Other Teaching Professionals",
    "231": "Economists, Accountants and Auditors",
    "232": "Legal Professionals",
    "233": "Archivists, Librarians and Information Professionals",
    "234": "Social Professionals",
    "235": "Religious Professionals",
    "241": "Sales and Marketing Professionals",
    "242": "Business and Administration Professionals",
    "243": "Finance Professionals",
    "244": "Administrative Professionals",
    "245": "ICT Professionals",
    "251": "Software and Applications Developers and Analysts",
    "252": "Database and Network Professionals",
    "261": "Legal Professionals (Advanced)",
    "262": "Librarians and Related Information Professionals",
    "263": "Social and Behavioral Science Professionals",
    "264": "Writers, Journalists and Linguists",
    "265": "Creative and Performing Artists",
    # 3 - Technicians and Associate Professionals
    "311": "Physical and Engineering Science Technicians",
    "312": "Mining, Manufacturing and Construction Supervisors",
    "313": "Process Control Technicians",
    "314": "Life Science Technicians",
    "315": "Marine and Flight Engineers",
    "321": "Medical and Pharmaceutical Technicians",
    "322": "Nursing and Midwifery Associate Professionals",
    "323": "Traditional and Complementary Medicine Professionals",
    "324": "Veterinary Technicians and Assistants",
    "331": "Financial and Mathematical Associate Professionals",
    "332": "Insurance and Real Estate Sales Agents",
    "333": "Commercial Sales Representatives",
    "334": "Administrative Secretaries",
    "335": "Government Regulatory Officials",
    "341": "Legal, Social and Religious Associate Professionals",
    "342": "Sports and Fitness Workers",
    "343": "Photographers and Image and Sound Recording Equipment Operators",
    "344": "Fashion and Interior Designers and Decorators",
    "345": "Chefs and Cooks",
    "351": "Information and Communications Technology Operations and User Support Technicians",
    "352": "Telecommunications and Broadcasting Technicians",
    "353": "Technical and Commercial Sales Representatives",
    # 4 - Clerical Support Workers
    "411": "General Office Clerks",
    "412": "Secretaries",
    "413": "Keyboard Operators",
    "421": "Finance and Accounting Clerks",
    "422": "Statistical, Finance and Insurance Clerks",
    "423": "Clerical Support Workers",
    "431": "Library and Filing Clerks",
    "432": "Personnel Clerks",
    "433": "Production and Logistics Clerks",
    "441": "Library and Mail Clerks",
    "442": "Coding, Proof-reading and Related Clerks",
    "443": "Clerical Supervisors",
    # 5 - Service and Sales Workers
    "511": "Travel Attendants and Travel Stewards",
    "512": "Cooks",
    "513": "Waiters and Bartenders",
    "514": "Hairdressers, Beauticians and Related Workers",
    "515": "Building and Housekeeping Supervisors",
    "516": "Other Personal Services Workers",
    "521": "Street Food and Market Salespersons",
    "522": "Shop Salespersons",
    "523": "Cashiers and Ticket Clerks",
    "524": "Other Sales Workers",
    "531": "Child Care Workers and Teachers' Aides",
    "532": "Personal Care Workers in Health Services",
    "541": "Protective Services Workers",
    "551": "Sports and Fitness Workers",
    "552": "Pet Care and Related Workers",
    # 6 - Agricultural and Fishery Workers
    "611": "Market Gardeners and Crop Producers",
    "612": "Animal Producers",
    "613": "Mixed Crop and Animal Producers",
    "621": "Forestry and Related Workers",
    "622": "Fishery Workers, Hunters and Trappers",
    "631": "Subsistence Crop Farmers",
    "632": "Subsistence Livestock Farmers",
    "633": "Subsistence Mixed Crop and Livestock Farmers",
    "634": "Subsistence Fishers, Hunters and Gatherers",
    # 7 - Craft and Related Trades Workers
    "711": "Miners, Shotfirers, Stone Cutters and Carvers",
    "712": "Building Frame and Related Trades Workers",
    "713": "Building Finishers and Related Trades Workers",
    "714": "Painters, Building Structure Cleaners and Related Trades Workers",
    "721": "Metal Moulders and Core Makers",
    "722": "Blacksmiths, Toolmakers and Related Trades Workers",
    "723": "Machinery Mechanics and Repairers",
    "724": "Electrical Equipment Installers and Repairers",
    "731": "Precision Instrument Makers and Repairers",
    "732": "Jewellery and Precious Metal Workers",
    "733": "Crafts Workers",
    "734": "Printing and Related Trades Workers",
    "741": "Food Processing and Related Trades Workers",
    "742": "Wood Treaters, Cabinet-makers and Related Trades Workers",
    "751": "Textiles, Garments and Leather Trades Workers",
    "752": "Footwear and Leather Goods Makers",
    # 8 - Plant and Machine Operators and Assemblers
    "811": "Mining and Mineral Processing Plant Operators",
    "812": "Metal Processing and Finishing Plant Operators",
    "813": "Glass, Ceramics and Related Plant Operators",
    "814": "Chemical Products Plant and Machine Operators",
    "815": "Rubber, Plastics and Paper Products Machine Operators",
    "816": "Textile, Fur and Leather Products Machine Operators",
    "817": "Wood Products Plant and Machine Operators",
    "818": "Other Plant and Machine Operators",
    "821": "Metal Products Machine Operators",
    "822": "Wood Products Machine Operators",
    "823": "Chemical Products Machine Operators",
    "824": "Rubber and Plastics Products Machine Operators",
    "825": "Printing and Binding Machine Operators",
    "826": "Textile Products Machine Operators",
    "827": "Leather Products Machine Operators",
    "828": "Assemblers",
    "831": "Locomotive Engine Drivers and Related Workers",
    "832": "Car, Van and Motorcycle Drivers",
    "833": "Heavy Truck and Bus Drivers",
    "834": "Mobile Farm and Heavy Plant Machinery Drivers",
    "835": "Ships' Deck Crews and Related Workers",
    # 9 - Elementary Occupations
    "911": "Domestic, Hotel and Office Cleaners and Helpers",
    "912": "Vehicle, Window, Laundry and Other Hand Cleaning Workers",
    "921": "Agricultural, Fishery and Related Labourers",
    "922": "Mining, Construction, Manufacturing and Transport Labourers",
    "931": "Manufacturing Labourers",
    "932": "Transport and Storage Labourers",
    "941": "Food Preparation Assistants",
    "942": "Street and Related Services Workers",
    "951": "Computing Equipment, Furniture and Sports Equipment Controllers",
    "952": "Packagers and Hand Packers",
    "961": "Refuse Workers and Other Elementary Workers",
    "962": "Messengers, Porters, Doorkeepers and Related Workers",
    # 0 - Armed Forces
    "011": "Armed Forces",
}

CATEGORY_MAPPING = {
    "1": "Managers",
    "2": "Professionals",
    "3": "Technicians & Associates",
    "4": "Clerical Support",
    "5": "Service & Sales",
    "6": "Agriculture & Fishery",
    "7": "Craft & Trades",
    "8": "Machine Operators",
    "9": "Elementary",
    "0": "Armed Forces",
}


def get_category(nco_code):
    """Get category from NCO code"""
    if len(nco_code) >= 1:
        first_digit = nco_code[0]
        return CATEGORY_MAPPING.get(first_digit, "Other")
    return "Other"


def get_occupation_name(nco_code):
    """Get occupation name from NCO code"""
    return NCO_MAPPING.get(nco_code, f"Unknown Occupation ({nco_code})")


def get_occupation_with_code(nco_code):
    """Get occupation name with code"""
    name = get_occupation_name(nco_code)
    return f"{name} ({nco_code})"


if __name__ == "__main__":
    print("NCO 2015 Mapping for India Job Market Visualizer")
    print("=" * 50)
    print(f"Total mappings: {len(NCO_MAPPING)}")
    print(f"\nCategories:")
    for code, name in CATEGORY_MAPPING.items():
        print(f"  {code}: {name}")
    print("\nSample mappings:")
    for code in list(NCO_MAPPING.keys())[:10]:
        print(f"  {code}: {NCO_MAPPING[code]}")
