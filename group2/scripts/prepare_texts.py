# Script to generate or prepare text data
# Note: Harry Potter books are copyrighted. 
# This script assumes you have legally obtained the text files.
# Place .txt files in ../datasets/texts/

import os

texts_dir = '../datasets/texts'
os.makedirs(texts_dir, exist_ok=True)

print("Place Harry Potter book text files in ../datasets/texts/")
print("Expected format: book1.txt, book2.txt, etc.")
print("Each file should contain the full text of one book.")

# Example: If you have the texts, you can add preprocessing here
# For demonstration, create sample text
sample_text = """
Harry Potter was a wizard. Hermione was smart. Ron was brave. 
Dumbledore was wise. Snape was mysterious. Voldemort was evil.
"""

with open(os.path.join(texts_dir, 'sample_book.txt'), 'w') as f:
    f.write(sample_text)

print("Sample text created. Replace with actual book texts for full analysis.")
