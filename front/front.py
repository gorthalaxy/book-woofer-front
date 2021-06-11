import streamlit as st
import requests
import matplotlib.pyplot as plt
from ebook import *
import io


st.title('books and woofers')

# uploaded_file = st.file_uploader("Choose an ebook")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is None:
    st.text("Where is your file?")
else:
    g = io.BytesIO(uploaded_file.read())  # BytesIO Object
    temporary_location = "temp.epub"
    with open(temporary_location, 'wb') as out:  # Open temporary file as bytes
        out.write(g.read())  # Read bytes into file
        # close file
        out.close()
    ready = KindleText("temp.epub").epub2text()
    st.text(ready[0])

user_input = st.text_input('Enter a sentence : ')

#====================Send request and print prediction

texts =  {'text' : user_input}
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
    