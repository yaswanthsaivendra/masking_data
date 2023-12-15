import re

def ner_mask(text,ner):
  ner_doc = ner(text)
  to_mask = []
  for i in ner_doc:
    if i["entity"] in ["B-LOC","I-LOC","I-PER","B-PER"]:
      to_mask.append(i["word"])

  for i in to_mask:
    text = text.replace(i,"*")
  return text


def mask_emails(text):
    match = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', text)
    s = match
    if s and len(s)>0:
        for i in s:
            text = text.replace(i,"*****")
    return text

def mask_phone_numbers(text):
    """
        000-000-0000
        000 000 0000
        000.000.0000

        (000)000-0000
        (000)000 0000
        (000)000.0000
        (000) 000-0000
        (000) 000 0000
        (000) 000.0000

        000-0000
        000 0000
        000.0000
        0000000
        0000000000
        (000)0000000

        # Detect phone numbers with country code
        +00 000 000 0000
        +00.000.000.0000
        +00-000-000-0000
        +000000000000
        0000 0000000000
        0000-000-000-0000
        00000000000000
        +00 (000)000 0000
        0000 (000)000-0000
        0000(000)000-0000 
    """
    masked_phones = []
    match = re.findall(r'((?:\+\d{2}[-\.\s]??|\d{4}[-\.\s]??)?(?:\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}))', text)
    for i in match:
        masked_phones.append(i)
        text = text.replace(i,"*****")
    return text

def mask_private_info(text,ner):
    try:
        text = str(text)
        text = mask_emails(text)
        text = mask_phone_numbers(text)
        text = ner_mask(text,ner)
    except Exception as e:
        print(f"masking skipped for text = {text}")
    return text