import re

#
# FUNCTIONS RETURNS A CHARACTERISTIC FOR A TEXT BLOCK
#

def get_confidence(block: dict) -> float:
    return block['confidence']

def is_capitalized(block: dict) -> bool:
    return block['text'].istitle() or block['text'].isupper()

def has_price_format(block: dict) -> bool:
    price_pattern = re.compile(r"""
    (?<!\w)                  # Negative lookbehind to ensure it's not part of a word
    [\$€£¥]?                 # Optional currency symbol
    \s*                      # Optional space between currency symbol and number
    (?:                      # Non-capturing group for the number
        \d{1,3}              # 1-3 digits
        (?:,\d{3})*          # Optional comma followed by exactly 3 digits (e.g., 1,000 or 1,000,000)
        |                    # OR
        \d+                  # Just digits (no comma format)
    )
    (?:\.\d{2})?             # Optional decimal point followed by exactly 2 digits
    (?!\w)                   # Negative lookahead to ensure it's not part of a word
""", re.VERBOSE)

    return bool(price_pattern.search(block['text'])) or block['text']

def has_date_format(block: dict) -> bool:
    # yyyy-mm-dd, yyyy/mm/dd, yyyy.mm.dd
    # mm/dd/yyyy or m/d/yyyy
    date_pattern = r'''
    (?<!\d)              # Not preceded by a digit
    (                    # Start of group
        (?:              # Non-capturing group for format types
            \d{1,2}       # Day or Month
            [/\-.]        # Separator
            \d{1,2}       # Month or Day
            [/\-.]        # Separator
            \d{2,4}       # Year
        )
        |
        (?:              # ISO or YYYY.MM.DD
            \d{4}
            [/\-.]
            \d{1,2}
            [/\-.]
            \d{1,2}
        )
        |
        (?:              # Month name formats
            (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|
             January|February|March|April|May|June|July|August|
             September|October|November|December)
            [\s\-]?
            \d{1,2}
            ,?
            \s?
            \d{4}
        )
        |
        (?:              # Day-MonthName-Year
            \d{1,2}
            [\s\-]?
            (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|
             January|February|March|April|May|June|July|August|
             September|October|November|December)
            ,?
            \s?
            \d{4}
        )
    )
    (?!\d)               # Not followed by a digit
'''

    match = re.search(date_pattern, block['text'], re.IGNORECASE | re.VERBOSE)
    return bool(match)

def has_phone_format(block: dict) -> bool:
    phone_pattern = re.compile(r"""
    ^\s*                             # optional leading whitespace
    (\+?\d{1,3})?                    # optional country code, e.g., +1, +44
    [\s\-\.]?                        # optional separator
    (\(?\d{3}\)?|\d{2,4})            # area code, with or without parentheses
    [\s\-\.]?                        # optional separator
    \d{3,4}                          # local part 1
    [\s\-\.]?                        # optional separator
    \d{4}                            # local part 2
    \s*$                             # optional trailing whitespace
""", re.VERBOSE)
    
    return bool(phone_pattern.search(block['text']))

def has_total_price_words(block: dict) -> bool:
    words = ['TOTAL', 'BAL', 'BALANCE']
    return any(term in block['text'].upper() for term in words)

def get_coords(block: dict) -> tuple:
    x_min = block['bbox'][0][0]
    y_min = block['bbox'][0][1]
    x_max = block['bbox'][2][0]
    y_max = block['bbox'][2][1]

    return (x_min, y_min, x_max, y_max)

def get_y_pos_norm(block: dict, image_height: int) -> float:
    _, y_min, _, y_max = get_coords(block)
    center_y = (y_min + y_max) / 2
    return center_y / image_height

def get_x_pos_norm(block: dict, image_width: int) -> float:
    x_min, _, x_max, _ = get_coords(block)
    center_x = (x_min + x_max) / 2
    return center_x / image_width

def is_center_aligned(block: dict, image_width: int, tolerance=0.2) -> bool:
    x_min, _, x_max, _ = get_coords(block)
    center_x = (x_min + x_max) / 2
    return abs(center_x - image_width / 2) < (image_width * tolerance)

def get_area_norm(block: dict, entries: list) -> float:
    min_area, max_area = get_min_max_area(entries)
    block_area = (get_coords(block)[2] - get_coords(block)[0]) * (get_coords(block)[3] - get_coords(block)[1])
    return (block_area - min_area) / (max_area - min_area)

#
# FUNCTIONS RETURN VALUES NEEDED FOR NORMALIZATION
#

def get_min_max_area(entries: list) -> tuple:
    areas = []
    for block in entries:
        x_min, y_min, x_max, y_max = get_coords(block)
        areas.append((x_max - x_min) * (y_max - y_min))

    return (min(areas), max(areas))

#
# HELPER FUNCTIONS FOR FEATURES
#

# returns list of text within receipt that are prices in ascending order
def extract_and_sort_prices(entries: list) -> list:
    price_pattern = re.compile(r"""
    (?<!\w)                  # Negative lookbehind to ensure it's not part of a word
    [\$€£¥]?                 # Optional currency symbol
    \s*                      # Optional space between currency symbol and number
    (?:                      # Non-capturing group for the number
        \d{1,3}              # 1-3 digits
        (?:,\d{3})*          # Optional comma followed by exactly 3 digits (e.g., 1,000 or 1,000,000)
        |                    # OR
        \d+                  # Just digits (no comma format)
    )
    (?:\.\d{2})?             # Optional decimal point followed by exactly 2 digits
    (?!\w)                   # Negative lookahead to ensure it's not part of a word
""", re.VERBOSE)

    matched_prices = []

    for e in entries:
        match = price_pattern.fullmatch(e['text'].strip())
        if match:
            raw = match.group()
            normalized = raw.replace(',', '').replace('$', '').replace('€', '').replace('£', '').replace('¥', '').strip()
            try:
                value = float(normalized)
                matched_prices.append((raw, value))
            except ValueError:
                continue

    # Sort descending by numeric value
    sorted_prices = sorted(matched_prices, key=lambda x: x[1])
    
    # Return only the original matching strings
    return [price[0] for price in sorted_prices]

# returns the y position of the text block with the word "total", "balance", etc.
def get_total_y_pos(entries: list, image_height: int) -> float:
    for block in entries:
        if has_total_price_words(block):
            return get_y_pos_norm(block, image_height)
    
    return None # type: ignore

#
# SCORING FUNCTIONS FOR EACH FEATURE
#

def store_name_score(block: dict, image_height: int, image_width: int, entries: list, weights: dict) -> dict:
    score_debug = {
        'TEXT': block['text'],
        '+Y POS': 1 - get_y_pos_norm(block, image_height),
        '+BBOX AREA': get_area_norm(block, entries),
        '+CAPITALIZE': int(is_capitalized(block)),
        '+CENTER ALIGNED': int(is_center_aligned(block, image_width)),
        '+CONFIDENCE': get_confidence(block),
        '-PRICE FORMAT': int(has_price_format(block)),
        '-DATE FORMAT': int(has_date_format(block)),
        '-PHONE FORMAT': int(has_phone_format(block))
    }

    return score_debug

def date_score(block: dict, weights: dict) -> dict:
    score_debug = {
        'TEXT': block['text'],
        '+DATE FORMAT': int(has_date_format(block))
    }

    return score_debug

def total_price_score(block: dict, image_height: int, image_width: int, entries: list, weights: dict) -> dict:
    prices = extract_and_sort_prices(entries)

    try:
        price_index = prices.index(block['text'])
    except ValueError:
        price_index = 0

    total_y = get_total_y_pos(entries, image_height)
    total_y_closeness = 0
    if total_y is not None:
        total_y_closeness = 1.0 - abs(total_y - get_y_pos_norm(block, image_height))

    score_debug = {
        'TEXT': block['text'],
        '+PRICE ORDER': price_index,
        '+TOTAL Y CLOSENESS': total_y_closeness,
        '+RIGHT SIDE': int(get_x_pos_norm(block, image_width) > 0.5)
    }

    return score_debug


