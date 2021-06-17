#----------------------------------------
#   BOOK WOOFER FRONT
#----------------------------------------​
import string
import streamlit as st
import requests
import matplotlib.pyplot as plt
from ebook import *
import io
import string
from spotifywidget import *
from load_css import local_css


# f = f'''<style>.myDiv {{border: 5px double DarkOliveGreen;background-color: Cornsilk; text-align: center; padding: 20px;}}</style></head><body><div class="myDiv"><p style="color:Black; text-align:left">hello</p></div>'''



#   Head
#----------------------------------------

st.set_page_config(layout="wide")
st.title('Book Woofer')
# local_css("style.css")
 
#pantone Palette
#blue = C3D7EE = fear
#pink = DCC5C4 = love
#dusky orange = F2C6AB = anger
#green = 93E6B4 = neutral
#yellow = F3EAA1 = happy
#egg shell = DDE4E6 = sadness
mood_colors = {'anger': 'F2C6AB', 
               'fear': 'C3D7EE' , 
               'happy': 'F3EAA1', 
               'love': 'DCC5C4', 
               'neutral': '93E6B4', 
               'sadness': '9BB7D4'}

# mood_colors = {'anger': '7B241C', 'fear': '212F3C', 'happy': 'AF601A', 'love': '5B2C6F', 'neutral': '4D5656', 'sadness': '154360'}
make_choice = st.sidebar.selectbox('Options:', ['Upload Ebook', 'Select Ebook', 'Upload Text'])
# user = User
# playing = Playback
# playlist = Playlists
# st.sidebar.write(playing.currently_playing())
# st.sidebar.write(user.user_id())
# st.sidebar.write(user.user_followers())
#----------------------------------------
#   Ebook
#----------------------------------------
if make_choice == 'Upload Ebook':
    # try:
        # col1, col2, = st.beta_columns((3,1))
        # with col1 :
            uploaded_file = st.file_uploader("Upload your ebook.")
            temporary_location = False
            if uploaded_file is not None:
                g = io.BytesIO(uploaded_file.read())  # BytesIO Object
                temporary_location = "testout_simple.epub"
                print(temporary_location)
                with open(temporary_location, 'wb') as out:  # Open temporary file as bytes
                    out.write(g.read())  # Read bytes into file
                    output = read_book(temporary_location)
                    st.markdown("<div id='linkto_top'></div>", unsafe_allow_html=True)
                    chapter = st.selectbox(
                        'Chapter:', [i+1 for i in range(len(output))])
                    # Chapter -1 for real index
                    chapter = chapter-1
                    # Remove punctuation for prediction
                    string.punctuation = string.punctuation+"“”"
                    out = "".join([element for element in output[chapter] if element not in string.punctuation])
                    # raw_string = r"{}".format(output[chapter])
                    
                    st.markdown(output[chapter])
                    # print(output[chapter])
#                     st.text(type(output))
#                     f = '''<style>.myDiv {border: 5px double DarkOliveGreen;background-color: Cornsilk;
#                     text-align: center; padding: 200px;}
# </style>
# <div class="myDiv"><p style="color:Black; text-align:left">'''
#                     st.markdown(f, unsafe_allow_html=True)
#                     st.markdown(output[chapter], unsafe_allow_html=True)
#                     st.markdown('</p></div>', unsafe_allow_html=True)
        #====================Send request and print prediction
                    texts = {'text': out}
                    url = "https://bfcontainer-csy3ocxwaq-ew.a.run.app/predict/"
                    response = requests.post(
                        url,
                        params=texts,
                    ).json()
                    st.text(response)
                    st.markdown("<a href='#linkto_top' style='color:#FFFFFF'>Choose next chapter!</a>", unsafe_allow_html=True)
                our_mood = max(response, key=response.get)
                st.set_option('deprecation.showPyplotGlobalUse', False)
                # sidebar_css = """<style>.sidebar .sidebar-content {background-image: linear-gradient(#FFFFFF,#FFFFFF);color: white;}</style>"""
                # st.markdown(sidebar_css,unsafe_allow_html=True)
                with st.sidebar:
                    # sidebar_css = """<style>.sidebar .sidebar-content {background-image: linear-gradient(#FFFFFF,#FFFFFF);color: white;}</style>"""
                    # st.markdown(sidebar_css,unsafe_allow_html=True)
                    fig = plt.figure()
                    fig.patch.set_facecolor(f'#{mood_colors[our_mood]}')
                    fig.patch.set_alpha(1)#0.6)
                    ax = fig.add_subplot(111)
                    ax.patch.set_facecolor('white')
                    ax.patch.set_alpha(1)#0.6)
                    ax.tick_params(axis='both', colors='black', labelsize=12)
                    plt.bar(x = response.keys(), height = response.values(), color = f'#{mood_colors[our_mood]}')
                    st.markdown(f"<h3 style='text-align: center; color: white;'>Current Mood: {our_mood.title()}</h1>", unsafe_allow_html=True)
                    st.pyplot()
                    
                    select_playlist(our_mood)
                # st.markdown(
                # f"""
                # <style>
                # .reportview-container {{
                #     background: #{mood_colors[our_mood]}
                # }}
                # </style>
                # """,
                # unsafe_allow_html=True
                # )
    # except:
    # # Prevent the error from propagating into your Streamlit app.
    #     pass
#----------------------------------------
#   Upload Text
#----------------------------------------
if make_choice == 'Upload Text':
    # try:
        # col1, col2, = st.beta_columns((3,1))
        # with col1 :
            input_object = st.text_input('Enter a sentence, a paragraph or more: ')
            if len(input_object) > 1:
                param_object = [input_object]
        #====================Send request and print prediction
                texts =  {'text' : param_object}
                url = "https://bfcontainer-csy3ocxwaq-ew.a.run.app/predict/"
                response = requests.post(
                    url,
                    params=texts,
                ).json()
                st.markdown(input_object)
                # t = f"<div><span class='highlight blue'>{input_object}</span>"
                # k = '<div style=width:200px;height:100px;border:6px>text</div>'
                # f = f'''<style>.myDiv {{border: 5px double DarkOliveGreen;background-color: Cornsilk; padding: 20px;}}</style><div class="myDiv"><p style="color:Black; text-align:left">{input_object}</p></div>'''


                # st.markdown(f, unsafe_allow_html=True)
                
        # mood_colors = {'anger': 'B52525', 'fear': '489D38' , 'happy': 'DAC623', 'love': '9C37AA', 'neutral': '155249', 'sadness': '3298D5'}
        # our_mood = max(response, key=response.get)
        # select_playlist(our_mood)
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
        # with col2:
            if len(input_object) > 1:
                param_object = [input_object]
                our_mood = max(response, key=response.get)
                st.set_option('deprecation.showPyplotGlobalUse', False)
                with st.sidebar:
                    fig = plt.figure()
                    fig.patch.set_facecolor(f'#{mood_colors[our_mood]}')
                    fig.patch.set_alpha(1)#0.6)
                    ax = fig.add_subplot(111)
                    ax.patch.set_facecolor('white')
                    ax.patch.set_alpha(1)#0.6)
                    ax.tick_params(axis='both', colors='black', labelsize=12)
                    plt.bar(x = response.keys(), height = response.values(), color = f'#{mood_colors[our_mood]}')
                    st.markdown(f"<h3 style='text-align: center; color: white;'>Current Mood: {our_mood.title()}</h1>", unsafe_allow_html=True)
                    st.pyplot()
                    select_playlist(our_mood)
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
    # except:
    # # Prevent the error from propagating into your Streamlit app.
    #     pass
# mood_colors = {'anger': 'B52525', 'fear': '489D38' , 'happiness': 'DAC623', 'love': '9C37AA', 'neutral': '155249', 'sadness': '3298D5'}

# with col2:
#     st.set_option('deprecation.showPyplotGlobalUse', False)
#     plt.bar(x = response.keys(), height = response.values())
#     st.pyplot()
#     our_mood = max(response, key=response.get)
#     # select_playlist(our_mood)
#     if response is not None:
#         st.markdown(
#         f"""
#         <style>
#         .reportview-container {{
#             background: #{mood_colors[our_mood]}
#         }}
#         </style>
#         """,
#         unsafe_allow_html=True
#     )

#----------------------------------------
#   Upload Text
#----------------------------------------
if make_choice == 'Select Ebook':
    book_choice = st.selectbox('Which book', ['Alices Adventures in Wonderland', 'The White Feather'])
    output = read_book(f'{book_choice}.epub')
    chapter = st.selectbox('Chapter:', [i+1 for i in range(len(output))])
    chapter = chapter-1
    string.punctuation = string.punctuation+"“”"
    out = "".join([element for element in output[chapter] if element not in string.punctuation])
    texts = {'text': out}
    url = "https://bfcontainer-csy3ocxwaq-ew.a.run.app/predict/"
    response = requests.post(
        url,
        params=texts,
    ).json()
    st.markdown(output[chapter])
    st.text(response)
    st.markdown("<a href='#linkto_top' style='color:#FFFFFF'>Choose next chapter!</a>", unsafe_allow_html=True)
    our_mood = max(response, key=response.get)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    with st.sidebar:
        fig = plt.figure()
        fig.patch.set_facecolor(f'#{mood_colors[our_mood]}')
        fig.patch.set_alpha(1)#0.6)
        ax = fig.add_subplot(111)
        ax.patch.set_facecolor('white')
        ax.patch.set_alpha(1)#0.6)
        ax.tick_params(axis='both', colors='black', labelsize=12)
        plt.bar(x = response.keys(), height = response.values(), color = f'#{mood_colors[our_mood]}')
        st.markdown(f"<h3 style='text-align: center; color: white;'>Current Mood: {our_mood.title()}</h1>", unsafe_allow_html=True)
        st.pyplot()
        select_playlist(our_mood)