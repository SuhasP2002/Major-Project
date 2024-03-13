import contractions
import re
import inflect

def text_lower(data):
    return data.lower()

def contraction_replace(data):
    if isinstance(data, list):
        # If the input is a list, apply contractions.fix to each element
        return [contractions.fix(item) for item in data]
    else:
        # If the input is a string, apply contractions.fix directly
        return contractions.fix(data)

def number_to_text(data):
    temp_str = data.split()
    string = []
    for i in temp_str:
        if i.isdigit():
            temp = inflect.engine().number_to_words(i)
            string.append(temp)
        else:
            string.append(i)
    return ' '.join(string)

def clean_text(text):
    text = re.sub(r'\[.*?\]', ' ', text)
    text = re.sub(r'\W+', ' ', text)
    text = re.sub(r'\s{2,}', ' ', text)
    text = text.replace("[^a-zA-Z]", " ")
    return text.strip()

def preprocess_transcript(data):
    text = text_lower(data)
    text = number_to_text(text)
    text = contraction_replace(text)
    text = clean_text(text)
    return text