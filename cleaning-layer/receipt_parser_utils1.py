import re

"""
FUNCTIONS RETURNS A CHARACTERISTIC FOR A TEXT BLOCK
"""

def get_confidence(block: dict) -> float:
    return block['confidence']

def is_capitalized(block: dict) -> bool:
    return block['text'].istitle() or block['text'].isupper()

def has_price_format(block: dict) -> bool:
    price_pattern = re.compile(r"""^[$€£¥]?\d+(\.\d{1,2})?$""")

    return bool(price_pattern.match(block['text']))

def has_date_format(block: dict) -> bool:
    # yyyy-mm-dd, yyyy/mm/dd, yyyy.mm.dd
    # mm/dd/yyyy or m/d/yyyy
    date_pattern = date_pattern = re.compile(r"""^((\d{4})[-/.](0?[1-9]|1[0-2])[-/.](0?[1-9]|[12][0-9]|3[01])|(0?[1-9]|1[0-2])[/\-\.](0?[1-9]|[12][0-9]|3[01])[/\-\.](\d{4})|(0?[1-9]|[12][0-9]|3[01])[.\-/](0?[1-9]|1[0-2])[.\-/](\d{4}))$""", re.VERBOSE)

    return bool(date_pattern.match(block['text']))

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
    
    return bool(phone_pattern.match(block['text']))

def get_coords(block: dict) -> tuple:
    x_min = block['bbox'][0][0]
    y_min = block['bbox'][0][1]
    x_max = block['bbox'][2][0]
    y_max = block['bbox'][2][1]

    return (x_min, y_min, x_max, y_max)

def get_y_pos_norm(block: dict, image_height: int) -> float:
    y_min, _, y_max, _ = get_coords(block)
    center_y = (y_min + y_max) / 2
    return center_y / image_height

def is_center_aligned(block: dict, image_width: int, tolerance=0.2) -> bool:
    x_min, _, x_max, _ = get_coords(block)
    center_x = (x_min + x_max) / 2
    return abs(center_x - image_width / 2) < (image_width * tolerance)

def get_area_norm(block: dict, entries: list) -> float:
    min_area, max_area = get_min_max_area(entries)
    block_area = (get_coords(block)[2] - get_coords(block)[0]) * (get_coords(block)[3] - get_coords(block)[1])
    return (block_area - min_area) / (max_area - min_area)

"""
FUNCTIONS RETURN VALUES NEEDED FOR NORMALIZATION
"""

def get_min_max_area(entries: list) -> tuple:
    areas = []
    for block in entries:
        x_min, y_min, x_max, y_max = get_coords(block)
        areas.append((x_max - x_min) * (y_max - y_min))

    return (min(areas), max(areas))

"""
SCORING FUNCTIONS FOR EACH FEATURE
"""

def store_name_score(block: dict, image_height: int, image_width: int, entries: list, weights: dict) -> dict:
    score_debug = {
        'TEXT': block['text'],
        '+Y POS': 1 - get_y_pos_norm(block, image_height),
        '+BBOX AREA': get_area_norm(block, entries),
        '+CAPITALIZE': is_capitalized(block),
        '+CENTER ALIGNED': is_center_aligned(block, image_width),
        '+CONFIDENCE': get_confidence(block),
        '-PRICE FORMAT': has_price_format(block),
        '-DATE FORMAT': has_date_format(block),
        '-PHONE FORMAT': has_phone_format(block)
    }

    return score_debug
