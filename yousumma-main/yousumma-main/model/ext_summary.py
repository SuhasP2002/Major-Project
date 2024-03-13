import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import re
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

def generate_extractive_summary(text):
    def replace_dot(input_string):
        return re.sub(r'\.(?!\s|$|\n)', 'dot', input_string)

    stop_words = set(stopwords.words('english'))
    text = text.lower()
    text = replace_dot(text)
    
    words = word_tokenize(text)
    word_freq = {}

    for word in words:
        if word in stop_words:
            continue
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1

    def add_period_after_n_words(text, n):
        words = text.split()
        result = ""
        for i, word in enumerate(words):
            result += word + " "
            if (i + 1) % n == 0 and i + 1 != len(words):
                result += ". "
        return result

    if '.' not in text:
        text = add_period_after_n_words(text, 10)

    sentences = sent_tokenize(text)
    sentence_ranking = {}

    for sentence in sentences:
        for word, freq in word_freq.items():
            if word in sentence:
                if sentence in sentence_ranking:
                    sentence_ranking[sentence] += freq
                else:
                    sentence_ranking[sentence] = freq

    rank_sum = sum(sentence_ranking.values())
    avg = int(rank_sum / len(sentence_ranking))

    summary = ''
    for sentence in sentences:
        if sentence_ranking[sentence] > (1 * avg):
            summary += ' ' + sentence

    return summary
