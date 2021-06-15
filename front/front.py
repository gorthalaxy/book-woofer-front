import streamlit as st
import requests
import matplotlib.pyplot as plt
from ebook import *
import io
from spotifywidget import select_and_play

st.set_page_config(layout="wide")

st.title('Book Woofer')



col1, col2, = st.beta_columns((3,1))

# uploaded_file = st.file_uploader("Choose an ebook")

with col1 :
    uploaded_file = st.file_uploader("Upload your kindle file.")
    temporary_location = False
    # param_object = 'I love apples'
    if uploaded_file is not None:
        g = io.BytesIO(uploaded_file.read())  # BytesIO Object
        temporary_location = "testout_simple.epub"
        print(temporary_location)
        with open(temporary_location, 'wb') as out:  # Open temporary file as bytes
            out.write(g.read())  # Read bytes into file
            output = read_book(temporary_location)
            chapter = st.selectbox(
                'Chapter:', [i+1 for i in range(len(output))])
            param_object = [chapter-1]
            st.markdown(output[chapter-1])

    input_object = st.text_input('Enter a sentence : ')
    if len(input_object) > 1:
        param_object = [input_object]

#====================Send request and print prediction

    texts =  {'text' : param_object}
    url = "https://bfcontainer-csy3ocxwaq-ew.a.run.app/predict/"
    response = requests.post(
        url,
        params=texts,
    ).json()
    st.text(response)

mood_colors = {'anger': 'B52525', 'fear': '489D38' , 'happy': 'DAC623', 'love': '9C37AA', 'neutral': '155249', 'sadness': '3298D5'}

# our_mood = max(response, key=response.get)
# select_and_play(our_mood)
# if response is not None:
#     st.markdown(
#     f"""
#     <style>
#     .reportview-container {{
#         background: #{mood_colors[our_mood]}
#     }}
#     </style>
#     """,
#     unsafe_allow_html=True
# )
# st.text(our_mood)

#plot your prediction

# components.html(
#     '''
#         <iframe src="https://open.spotify.com/embed/playlist/7xOHp3ZlSBJNJOgsQwF85S" width="300" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
#     ''',
#     height=600
# )

with col2:
    st.set_option('deprecation.showPyplotGlobalUse', False)
    plt.bar(x = response.keys(), height = response.values())
    st.pyplot()
    our_mood = max(response, key=response.get)
    select_and_play(our_mood)
    if response is not None:
        st.markdown(
        f"""
        <style>
        .reportview-container {{
            background: #{mood_colors[our_mood]}
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
