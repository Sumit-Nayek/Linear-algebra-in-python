## Challeges
#1. We have to read word file
#2. We have to convert the content in such a way that can be easly process for the counting of the conjunction
#3. After preparing the data we have to remove space and special chracter from the data.
#4. Now we have to transform all the data into lower or upper case , then we split into words
#5. Searching through the array of words and count the number of conjuctions


### First Approach

from docx import Document
import re
import string
def read_docx(file_path):
    """Reads text from a .docx file."""
    doc = Document(file_path)
    text = []
    for paragraph in doc.paragraphs:
        text.append(paragraph.text)
    return ''.join(text)

def count_conjunctions(text, conjunctions):
    lower_text = text.lower()   #Convert text to lowercase
    translator = str.maketrans('', '', string.punctuation)  #Remove punctuation from the text
    no_punctuation_text = lower_text.translate(translator)
    
    words = no_punctuation_text.split() #Split the cleaned text into a list of words
      
    return sum(1 for word in words if word in conjunctions)  #Count the conjunctions

docx_file="C:/Users/Student/Downloads/Test_file.docx"
output_file="C:/Users/Student/Downloads/output_text.txt"
conjunctions=['and', 'but', 'or', 'nor', 'for', 'yet', 'so']

# Read content from .docx file
document_text = read_docx(docx_file)

# Print text to a text file
with open(output_file, 'w') as f:
   f.write(document_text)
print(f"Content successfully written to {output_file}")

# Count conjunctions
conjunction_count = count_conjunctions(document_text, conjunctions)
print(f"Total number of conjunctions ({', '.join(conjunctions)}): {conjunction_count}")


