# Constants for CPI Book Price Calculation
PAPER_WEIGHT_80GMS = 0.0049
PAPER_WEIGHT_110GMS = 0.0124
PRINTING_COST_BW = 0.0062
PRINTING_COST_COLOR = 0.0198
HANDLING_FEE = 1.75
PULA_FEE = 5
COVER_COSTS = {
    "Soft Cover": 0.99,
    "Hard Cover": 4.21
}


def determine_paper_weight(total_pages):
    if total_pages <= 58:
        return "110 gms", PAPER_WEIGHT_110GMS
    return "80 gms", PAPER_WEIGHT_80GMS


def calculate_cpi_cost(total_pages, color_pages, copies, cover_type):
    try:
        if cover_type == "Soft":
            cover_type = "Soft Cover"
        elif cover_type == "Hard":
            cover_type = "Hard Cover"

        paper_weight, paper_cost_per_page = determine_paper_weight(total_pages)
        bw_pages = total_pages - color_pages
        bw_pages_cost = round(bw_pages * PRINTING_COST_BW, 2)
        color_pages_cost = round(color_pages * PRINTING_COST_COLOR, 2)
        paper_total_cost = (bw_pages + color_pages) * paper_cost_per_page
        printing_total_cost = bw_pages_cost + color_pages_cost
        cover_total_cost = COVER_COSTS[cover_type] * copies
        total_cost = round(
            (paper_total_cost + printing_total_cost) * copies + cover_total_cost, 2
        )

        return {
            "paper_weight": paper_weight,
            "bw_pages_cost": bw_pages_cost,
            "color_pages_cost": color_pages_cost,
            "cover_cost": cover_total_cost,
            "price_per_copy": round(total_cost / copies, 2),
            "total_cost": round(total_cost, 2)
        }
    except ValueError:
        raise ValueError("Invalid input data.")


# Constants for Shipping Calculation
max_weight = [
    0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10,
    11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
    35, 40, 45, 50, 55, 60, 65, 70
]
zone_1 = [
    25.72, 25.72, 26.41, 27.11, 27.82, 28.53, 30.97, 31.75, 32.49, 33.25, 33.83,
    34.41, 37.01, 37.63, 38.24, 38.87, 39.49, 40.10, 40.71, 41.34, 46.14, 47.38,
    48.62, 49.85, 51.08, 56.59, 57.93, 59.30, 60.66, 62.00, 65.80, 69.58, 71.00,
    72.45, 73.88, 75.33, 76.76, 78.21, 79.65, 81.08, 114.07, 131.95, 141.00, 150.03,
    159.07, 168.13, 191.14, 201.01
]
zone_2 = [
    25.93, 25.93, 26.98, 28.01, 29.01, 30.08, 33.05, 34.21, 35.34, 36.51, 37.50,
    38.48, 41.88, 42.94, 43.98, 45.03, 46.08, 47.13, 48.18, 49.22, 55.44, 57.13,
    58.80, 60.48, 62.17, 69.29, 71.09, 72.91, 74.71, 76.51, 81.67, 86.79, 88.84,
    90.91, 92.96, 95.02, 97.07, 99.12, 101.18, 103.23, 142.59, 167.46, 180.82,
    194.19, 207.56, 220.90, 252.95, 267.34
]
zone_3 = [
    27.46, 27.46, 28.99, 30.50, 32.03, 33.48, 37.13, 38.69, 40.27, 41.84, 43.32,
    44.77, 49.21, 50.79, 52.37, 53.94, 55.52, 57.13, 58.71, 60.28, 68.67, 71.41,
    74.17, 76.91, 79.68, 89.71, 92.76, 95.78, 98.83, 101.87, 109.08, 116.26, 119.31,
    122.36, 125.39, 128.43, 131.48, 134.51, 137.55, 140.59, 192.91, 232.76, 256.00,
    279.22, 302.45, 325.66, 378.08, 403.37
]
zone_4 = [
    27.04, 27.04, 28.47, 29.89, 31.29, 32.45, 35.61, 36.78, 37.94, 39.13, 40.11,
    41.15, 45.95, 47.07, 48.18, 49.29, 50.39, 51.50, 52.64, 53.73, 60.35, 62.35,
    64.35, 66.38, 68.39, 76.20, 78.40, 80.56, 82.74, 84.91, 90.38, 95.86, 98.08,
    100.29, 102.51, 104.74, 106.94, 109.19, 111.40, 113.60, 154.61, 181.12, 195.72,
    210.32, 224.91, 239.50, 278.77, 294.78
]
zone_5 = [
    29.26, 29.26, 31.04, 32.84, 34.61, 36.19, 40.22, 41.89, 43.59, 45.28, 46.61,
    47.91, 52.38, 53.79, 55.17, 56.59, 57.98, 59.39, 60.78, 62.17, 71.00, 74.02,
    77.02, 80.00, 83.00, 93.61, 96.93, 100.19, 103.48, 106.77, 114.47, 122.14,
    125.39, 128.63, 131.88, 135.13, 138.37, 141.62, 144.87, 148.12, 201.87, 243.37,
    267.22, 291.07, 314.92, 338.73, 393.00, 419.09
]
zone_6 = [
    29.83, 29.83, 31.65, 33.48, 35.32, 37.23, 41.18, 42.69, 44.18, 45.70, 47.05,
    48.40, 52.97, 54.43, 55.89, 57.33, 58.80, 60.27, 61.71, 63.18, 72.21, 75.34,
    78.48, 81.59, 84.72, 95.62, 99.02, 102.44, 105.84, 109.24, 117.06, 124.87,
    128.12, 131.37, 134.60, 137.86, 141.12, 144.35, 147.62, 150.84, 205.22, 247.56,
    272.01, 296.46, 320.92, 345.37, 400.88, 427.38
]
zone_7 = [
    29.96, 29.96, 31.62, 33.29, 34.95, 36.46, 40.38, 41.97, 43.57, 45.17, 46.42,
    47.65, 53.48, 54.89, 56.30, 57.74, 59.16, 60.57, 61.99, 63.39, 71.78, 74.58,
    77.38, 80.19, 82.98, 92.91, 95.96, 99.01, 102.05, 105.07, 112.12, 119.14, 122.09,
    125.07, 128.02, 131.00, 133.94, 136.87, 139.86, 142.83, 194.29, 233.35, 256.37,
    279.38, 302.40, 325.42, 383.18, 408.45
]
zone_8 = [
    32.00, 32.00, 34.00, 35.98, 37.98, 39.57, 43.83, 45.50, 47.19, 48.87, 50.28,
    51.66, 58.11, 59.62, 61.16, 62.65, 64.19, 65.70, 67.23, 68.74, 78.21, 81.52,
    84.86, 88.19, 91.52, 102.87, 106.48, 110.11, 113.70, 117.33, 125.60, 133.86,
    137.47, 141.09, 144.71, 148.33, 151.94, 155.55, 159.17, 162.80, 219.63, 264.01,
    290.11, 316.21, 342.30, 368.42, 434.81, 463.58
]
zone_9 = [
    33.86, 33.86, 36.32, 38.79, 41.25, 42.89, 47.45, 49.26, 51.04, 52.82, 54.64,
    56.43, 63.93, 65.91, 67.91, 69.90, 71.89, 73.88, 75.87, 77.89, 89.34, 93.69,
    98.05, 102.42, 106.77, 120.63, 125.35, 130.08, 134.79, 139.54, 150.04, 160.57,
    165.50, 170.43, 175.37, 180.31, 185.25, 190.16, 195.09, 200.03, 265.09, 318.51,
    349.35, 380.18, 411.01, 441.83, 520.96, 555.06
]
zone_10 = [
    36.11, 36.11, 39.36, 42.62, 45.90, 48.17, 53.85, 56.29, 58.73, 61.19, 63.63,
    66.06, 75.34, 78.05, 80.77, 83.47, 86.20, 88.91, 91.62, 94.34, 108.48, 113.82,
    119.16, 124.50, 129.85, 147.03, 152.86, 158.73, 164.55, 170.39, 184.31, 198.26,
    205.31, 212.40, 219.47, 226.51, 233.60, 240.65, 247.74, 254.81, 335.47, 406.57,
    448.29, 490.03, 531.75, 573.45, 679.31, 725.35
]
zone_11 = [
    40.25, 40.25, 43.83, 47.39, 50.98, 53.34, 59.56, 62.14, 64.71, 67.26, 69.83,
    72.40, 82.54, 85.37, 88.21, 91.05, 93.89, 96.72, 99.55, 102.38, 118.15, 124.36,
    130.52, 136.76, 142.97, 162.17, 168.90, 175.64, 182.38, 189.12, 203.83, 218.55,
    225.48, 232.44, 239.39, 246.33, 253.29, 260.22, 267.18, 274.11, 359.52, 435.97,
    480.56, 525.16, 569.76, 614.35, 728.23, 777.95
]

country_zone = {
    "Afghanistan": 11, "Albania": 8, "Algeria": 11, "American Samoa": 10,
    "Andorra": 8, "Angola": 11, "Anguilla": 10, "Antigua": 10,
    "Argentina": 11, "Armenia": 10, "Aruba": 10, "Australia": 9,
    "Austria": 3, "Azerbaijan": 10, "Bahamas": 10, "Bahrain": 10,
    "Bangladesh": 11, "Barbados": 10, "Belarus": 8, "Belgium": 1,
    "Belize": 11, "Benin": 11, "Bermuda": 10, "Bhutan": 11,
    "Bolivia": 11, "Bonaire": 10, "Bosnia": 8, "Botswana": 11,
    "Brazil": 11, "Brunei": 11, "Bulgaria": 6, "Burkina Faso": 11,
    "Burundi": 11, "Cambodia": 11, "Cameroon": 11, "Canada": 7,
    "Canary Islands": 6, "Cape Verde": 11, "Cayman Islands": 10,
    "Central African": 11, "Chad": 11, "Chile": 11, "China": 9,
    "Colombia": 11, "Comoros": 10, "Congo": 11, "Cook Islands": 10,
    "Costa Rica": 11, "Cote D'Ivoire": 10, "Croatia": 8, "Cuba": 10,
    "Curacao": 10, "Cyprus": 6, "Czech Republic": 5, "Denmark": 3,
    "Djibouti": 11, "Dominica": 10, "Dominican Republic": 10, "East Timor": 10,
    "Ecuador": 11, "Egypt": 10, "El Salvador": 11, "Eritrea": 11,
    "Estonia": 6, "Ethiopia": 11, "Falkland Islands": 10, "Faroe Islands": 8,
    "Fiji": 10, "Finland": 3, "France": 2, "French Guyana": 11,
    "Gabon": 11, "Gambia": 11, "Georgia": 10, "Germany": 2,
    "Ghana": 11, "Gibraltar": 8, "Greece": 3, "Greenland": 8,
    "Grenada": 10, "Guadeloupe": 11, "Guam": 10, "Guatemala": 11,
    "Guernsey": 6, "Guinea Republic": 11, "Guinea-Bissau": 11, "Guinea-Eq": 11,
    "Guyana British": 11, "Haiti": 11, "Honduras": 11, "Hong Kong": 9,
    "Hungary": 5, "Iceland": 8, "India": 9, "Indonesia": 9,
    "Iran": 10, "Iraq": 10, "Ireland": 1, "Israel": 10,
    "Italy": 3, "Jamaica": 10, "Japan": 9, "Jersey": 6,
    "Jordan": 11, "Kazakhstan": 10, "Kenya": 10, "Kiribati": 10,
    "Kosovo": 8, "Kuwait": 10, "Kyrgyzstan": 10, "Laos": 11,
    "Latvia": 6, "Lebanon": 11, "Lesotho": 11, "Liberia": 11,
    "Libya": 11, "Liechtenstein": 6, "Lithuania": 6, "Luxembourg": 1,
    "Macau": 9, "Macedonia": 8, "Madagascar": 11, "Malawi": 11,
    "Malaysia": 9, "Maldives": 11, "Mali": 11, "Malta": 6,
    "Marshall Islands": 10, "Martinique": 10, "Mauritania": 11, "Mauritius": 11,
    "Mayotte": 11, "Mexico": 7, "Micronesia": 10, "Moldova": 6,
    "Monaco": 2, "Mongolia": 10, "Montenegro": 6, "Montserrat": 11,
    "Morocco": 10, "Mozambique": 11, "Myanmar": 10, "Namibia": 11,
    "Nauru": 10, "Nepal": 11, "Netherlands": 1, "Netherlands Antilles": 11,
    "Nevis": 10, "New Caledonia": 10, "New Zealand": 10,
    "Nicaragua": 11, "Niger": 11, "Nigeria": 10, "Niue": 10,
    "Mariana Islands": 10, "North Korea": 10, "Norway": 6,
    "Oman": 10, "Pakistan": 10, "Palau": 11, "Panama": 11,
    "Papua New Guinea": 10, "Paraguay": 11, "Peru": 11,
    "Philippines": 9, "Poland": 5, "Portugal": 3, "Puerto Rico": 7,
    "Qatar": 10, "Reunion": 11, "Romania": 6, "Russia": 8,
    "Rwanda": 11, "Samoa": 10, "San Marino": 8, "Sao Tome & Princip": 10,
    "Saudi Arabia": 10, "Senegal": 11, "Serbia": 6, "Seychelles": 11,
    "Sierra Leone": 11, "Singapore": 9, "Slovakia": 5, "Slovenia": 5,
    "Solomon Islands": 10, "Somalia": 10, "Somaliland": 10,
    "South Africa": 9, "South Korea": 9, "South Sudan": 10,
    "Spain": 3, "Sri Lanka": 10, "St. Barthelemy": 10, "St. Eustatius": 10,
    "St. Helena": 10, "St. Kitts": 10, "St. Lucia": 10, "St. Maarten": 10,
    "St. Vincent": 10, "Sudan": 10, "Suriname": 11, "Swaziland": 11,
    "Sweden": 3, "Switzerland": 6, "Syria": 11, "Tahiti": 10,
    "Taiwan": 9, "Tajikistan": 10, "Tanzania": 11, "Thailand": 9,
    "Togo": 11, "Tonga": 10, "Trinidad & Tobago": 10, "Tunisia": 11,
    "Turkey": 8, "Turks & Caicos Isl.": 10, "Tuvalu": 11,
    "Uganda": 11, "Ukraine": 8, "United Arab Emirates": 9,
    "United States": 4, "Uruguay": 11, "Uzbekistan": 10, "Vanuatu": 10,
    "Vatican City": 3, "Venezuela": 11, "Vietnam": 10,
    "Virgin Islands": 10, "Yemen": 11, "Zambia": 11, "Zimbabwe": 10
}


def calculate_book_weight(page_count, cover_type):
    # Normalize the cover_type to handle both "Soft" and "Soft Cover", etc.
    if cover_type in ['Soft', 'Soft Cover']:
        cover_weight_gsm = 250
    elif cover_type in ['Hard', 'Hard Cover']:
        cover_weight_gsm = 500
    else:
        raise ValueError("Invalid cover type. Please enter 'Soft Cover' or 'Hard Cover'.")

    # Calculate the paper weight based on the page count
    if page_count <= 55:
        paper_weight_gsm = 110
    else:
        paper_weight_gsm = 80

    # Area in square meters (A4 paper dimensions)
    page_area_m2 = (152.4 / 1000) * (228.6 / 1000)
    cover_area_m2 = (152.4 / 1000) * (228.6 / 1000)

    # Calculate weights
    paper_weight_kg = (page_area_m2 * paper_weight_gsm * page_count / 2) / 1000
    cover_weight_kg = (cover_area_m2 * cover_weight_gsm * 2) / 1000

    total_book_weight_kg = paper_weight_kg + cover_weight_kg
    return total_book_weight_kg


def get_shipping_cost(weight, zone):
    zone_costs = {
        1: zone_1,
        2: zone_2,
        3: zone_3,
        4: zone_4,
        5: zone_5,
        6: zone_6,
        7: zone_7,
        8: zone_8,
        9: zone_9,
        10: zone_10,
        11: zone_11,
    }
    if zone not in zone_costs:
        return None

    costs = zone_costs[zone]
    for i, max_w in enumerate(max_weight):
        if weight <= max_w:
            return costs[i]
    return None


def calculate_order(total_pages, color_pages, copies, cover_type, country):
    if cover_type not in COVER_COSTS:
        cover_type = "Soft Cover"  # Default to "Soft Cover"

    cpi_cost = calculate_cpi_cost(total_pages, color_pages, copies, cover_type)
    book_weight_kg = calculate_book_weight(total_pages, cover_type) * copies
    zone = country_zone.get(country)

    if zone is not None:
        shipping_cost = get_shipping_cost(book_weight_kg, zone)
    else:
        shipping_cost = 'Not Available'

    if shipping_cost != 'Not Available':
        total_shipping_cost = shipping_cost + HANDLING_FEE + PULA_FEE
    else:
        total_shipping_cost = HANDLING_FEE + PULA_FEE

    total_cost = round(cpi_cost['total_cost'] + total_shipping_cost, 2)

    return {
        "price_per_copy": cpi_cost['price_per_copy'],
        "bw_pages_cost": cpi_cost['bw_pages_cost'],
        "color_pages_cost": cpi_cost['color_pages_cost'],
        "total_cost": total_cost,
        "total_weight": round(book_weight_kg, 3),
        "shipping_cost": total_shipping_cost
    }
