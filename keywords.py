import PyPDF2
import re, os
from collections import Counter
from nltk.corpus import stopwords

def remove_whitespace_from_sentence(sent):
    return " ".join(sent.split())

def clean_words(text):
    text = re.sub(r"what's", "what is ", text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"can't", "cannot ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"I'm", "I am", text)
    text = re.sub(r" m ", " am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r"\.com", "com ", text) # changing .com to com
    text = re.sub(r"\d", "", text)
    text = re.sub(r"\.", " . ", text)
    return text


def clean_punc(text):
    punc = "~`!@#$%^&*()-_+=:;,\'[]{}\\\/<>?\"|"

    for p in punc:
            text = text.replace(p, ' ')
    text = remove_whitespace_from_sentence(text)
    return text.lower()

def separate_words(word):
    tokens = []
    idx = 0
    for i in range(len(word)-1):
        w = ord(word[i])
        wi = ord(word[i+1])
        if ((w >= 65 and w <= 90) and (wi >= 97 and wi <= 122)):
            if word[idx:i] == '.':
                tokens.append(word[idx:i])
            else:
                if len(word[idx:i]) > 1:
                    tokens.append(word[idx:i])
            idx = i
    if word[idx:] == '.':
        tokens.append(word[idx:])
    else:
        if len(word[idx:]) > 1:
            tokens.append(word[idx:])
    return tokens

def remove_alphabet(keywords):
    new_key = []
    alphabet = [char for char in "abcdefghijklmnopqrstuvwxyz0123456789"]
    for key in keywords:
        if key not in alphabet:
            new_key.append(key)

    return new_key


if __name__ == "__main__":
    #filename = input("File path: ")
    filename = 'JavaBasics-notes.pdf'
    try:
        pdf_file = open(filename, 'rb')
    except Exception as e:
        print("Exception: ", e)
        exit()

    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    number_of_pages = read_pdf.getNumPages()

    pages = []

    for i in range(number_of_pages):
        page = read_pdf.getPage(i)
        page_content = page.extractText()
        page_content = ''.join([pc if ord(pc) < 128 else ' ' for pc in page_content])
        pages.append(str(page_content))

    text = ""

    for page in pages:
        text += remove_whitespace_from_sentence(clean_words(page))

    words = text.split(' ')

    keywords = []
    for word in words:
        new_words = separate_words(word)
        for w in new_words:
            keywords.append(w)

    keywords = remove_alphabet(keywords)

    stop_words = stopwords.words('english')
    stop_words = [clean_words(word) for word in stop_words]
    new_text = " ".join([word for word in keywords if not word in stop_words])
    new_text_formatted = clean_punc(new_text)

    ## Formatted sentences from PDF: new_text_formatted
    ## Save them to file
    file = open('pdf-data.txt', 'w')
    file.write(new_text_formatted)
    file.close()

    keywords = new_text_formatted.replace('.', '')
    keywords = remove_whitespace_from_sentence(keywords)
    keywords = keywords.split(' ')

    keywords_count = Counter(keywords)
    keywords_count_len = len(keywords_count.keys())
    print("Number of words: {0}".format(keywords_count_len))

    ## Creating a CSV file
    words_count = keywords_count.most_common(keywords_count_len)
    csv_file = open('word_count.csv', 'w')
    csv_file.write("Word, Frequency, Probability\n")
    for word in words_count:
        if len(word[0]) != 1:
            if word[0] not in stop_words:
                string = "{0}, {1}, {2}\n".format(word[0], word[1], float(word[1]/keywords_count_len))
                csv_file.write(string)
