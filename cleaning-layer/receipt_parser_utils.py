import re

def is_address_like(text: str) -> bool:
    return bool(re.search(r"\d{5}|\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\d+ [A-Za-z ]+ (St|Ave|Blvd|Rd|Ln|Dr)", text))

def is_blacklisted(text: str) -> bool:
    blacklist = ['RECEIPT', 'ORDER', 'CHANGE', 'TOTAL', 'STORE #', 'THANK YOU']
    return any(term in text.upper() for term in blacklist)

def is_title_or_caps(text: str) -> bool:
    return text.istitle() or text.isupper()

def is_center_aligned(f_bbox: tuple, image_width: int, tolerance=0.15) -> bool:
    x_min, _, x_max, _ = f_bbox
    center_x = (x_min + x_max) / 2
    return abs(center_x - image_width / 2) < (image_width * tolerance)

def bounding_box_area(f_bbox: tuple) -> int:
    x_min, y_min, x_max, y_max = f_bbox
    return (x_max - x_min) * (y_max - y_min)

# takes in unformatted block bbox
def get_bbox_coords(bbox: list) -> tuple[int, int, int, int]:
    # x_min, y_min, x_max, y_max
    return (bbox[0][0], bbox[0][1], bbox[2][0], bbox[2][1])

def score_text_block(block: dict, image_height: int, image_width: int, weights: dict) -> float:
    text = block['text']
    confidence = block['confidence']
    f_bbox = get_bbox_coords(block['bbox'])

    x_min, y_min, x_max, y_max = f_bbox
    norm_y = y_min / image_height
    area = bounding_box_area(f_bbox)
    center_aligned = is_center_aligned(f_bbox, image_width)
    caps = is_title_or_caps(text)
    address_like = is_address_like(text)
    blacklist = is_blacklisted(text)

    score = (
        weights['top'] * (1 - norm_y) +
        weights['area'] * area +
        weights['confidence'] * confidence +
        weights['center'] * int(center_aligned) +
        weights['caps'] * int(caps) -
        weights['address'] * int(address_like) -
        weights['blacklist'] * int(blacklist)
    )
    return score
