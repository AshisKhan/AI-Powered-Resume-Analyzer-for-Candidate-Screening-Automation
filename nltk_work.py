import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import re

'''
# Download the NLTK stopwords dataset (only once then make it comment!)
nltk.download('stopwords')
# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('wordnet')

'''
lemmatizer = WordNetLemmatizer()

def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    words = text.split()
    filtered_words = [word for word in words if word not in stop_words]
    return ' '.join(filtered_words)



def lemmatize_text(text):
    words = word_tokenize(remove_stopwords(text))
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    return ' '.join(lemmatized_words)





