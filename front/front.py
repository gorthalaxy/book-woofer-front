import streamlit as st
import requests
import matplotlib.pyplot as plt
from ebook import *
import io


st.title('books and woofers')

# uploaded_file = st.file_uploader("Choose an ebook")

uploaded_file = st.file_uploader("Upload your kindle file.")
temporary_location = False
if uploaded_file is not None:
  g = io.BytesIO(uploaded_file.read())  # BytesIO Object
  temporary_location = "testout_simple.epub"
  print(temporary_location)
  with open(temporary_location, 'wb') as out:  # Open temporary file as bytes
      out.write(g.read())  # Read bytes into file
      output = read_book(temporary_location)
      chapter = st.selectbox(
          'Chapter:', [i+1 for i in range(len(output))])
      st.markdown(output[chapter-1])

user_input = st.text_input('Enter a sentence : ')

#====================Send request and print prediction

texts =  {'text' : [chapter-1]}
url = "https://bfcontainer-csy3ocxwaq-ew.a.run.app/predict/"
response = requests.post(
    url,
    params=texts,
).json()
st.text(response)

#plot your prediction

st.set_option('deprecation.showPyplotGlobalUse', False)
plt.bar(x = response.keys(), height = response.values())
st.pyplot()
