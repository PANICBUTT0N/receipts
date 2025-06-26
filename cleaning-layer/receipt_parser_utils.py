import re

def is_address_like(text):
    return bool(re.search(r"\d{5}|\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\d+ [A-Za-z ]+ (St|Ave|Blvd|Rd|Ln|Dr)", text))

def is_blacklisted(text):
    blacklist = ['RECEIPT', 'ORDER', 'CHANGE', 'TOTAL', 'STORE #', 'THANK YOU']
    return any(term in text.upper() for term in blacklist)

def is_title_or_caps(text):
    return text.istitle() or text.isupper()

def is_center_aligned(bbox, image_width, tolerance=0.15):
    x_min, _, x_max, _ = bbox
    center_x = (x_min + x_max) / 2
    return abs(center_x - image_width / 2) < (image_width * tolerance)

def bounding_box_area(bbox):
    x_min, y_min, x_max, y_max = bbox
    return (x_max - x_min) * (y_max - y_min)

def score_text_block(block, image_height, image_width, weights):
    text = block['text']
    confidence = block['confidence']
    bbox = block['bbox']

    x_min, y_min, x_max, y_max = bbox
    norm_y = y_min / image_height
    area = bounding_box_area(bbox)
    center_aligned = is_center_aligned(bbox, image_width)
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
