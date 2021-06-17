#----------------------------------------
#   BOOK WOOFER FRONT
#----------------------------------------​
import string
import streamlit as st
import requests
import matplotlib.pyplot as plt
import seaborn as sns
from ebook import *
import io
import string
from spotifywidget import *
#----------------------------------------
#   Head
#----------------------------------------

st.set_page_config(layout="wide")
st.title('Book Woofer')
st.sidebar.title('Book Woofer')

user = User
playing = Playback
playlist = Playlists

#pantone Palette
#blue = C3D7EE = fear
#pink = DCC5C4 = love
#dusky orange = F2C6AB = anger
#green = 93E6B4 = neautral
#yellow = F3EAA1 = happy
#egg shell = DDE4E6 = sadness

mood_colors = {'anger': 'F2C6AB',
               'fear': 'C3D7EE' ,
               'happy': 'F3EAA1',
               'love': 'DCC5C4',
               'neutral': '93E6B4',
               'sadness': 'DDE4E6'}
make_choice = st.sidebar.selectbox('Options:', ['Upload Ebook', 'Upload Text'])
#st.sidebar.write(playing.currently_playing())
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
            st.markdown(output[chapter])
            #====================Send request and print prediction
            texts = {'text': out}
            url = "https://bfcontainer-csy3ocxwaq-ew.a.run.app/predict/"
            response = requests.post(
                url,
                params=texts,
            ).json()
            st.text(response)
            st.markdown("<a href='#linkto_top' style='color:#FFFFFF'>Go to the next chapter, or whichever one you want!</a>", unsafe_allow_html=True)
# with col2:
        our_mood = max(response, key=response.get)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        with st.sidebar:
            fig = plt.figure()
            fig.patch.set_facecolor(f'#{mood_colors[our_mood]}')
            fig.patch.set_alpha(0.6)
            ax = fig.add_subplot(111)
            ax.patch.set_facecolor('white')
            ax.patch.set_alpha(0.6)
            ax.tick_params(axis='both', colors='white', labelsize=12)
            plt.bar(x = response.keys(), height = response.values(), color ='purple')
            st.markdown(f"<h3 style='text-align: center; color: white;'>Current Mood: {our_mood.title()}</h1>", unsafe_allow_html=True)
            st.pyplot()

            select_playlist(our_mood)
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
# except:
# # Prevent the error from propagating into your Streamlit app.
#     pass
#----------------------------------------
#   Upload Text
#----------------------------------------
if make_choice == 'Upload Text':
    try:
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
        # with col2:
        if len(input_object) > 1:
            param_object = [input_object]
            our_mood = max(response, key=response.get)
            st.set_option('deprecation.showPyplotGlobalUse', False)
            with st.sidebar:

                # CIRCULAR BAR PLOT
                # set figure size
                plt.figure(figsize=(20,10))

                # plot polar axis
                ax = plt.subplot(111, polar=True)

                # remove grid
                plt.axis('off')

                df = pd.DataFrame({
                    'Name': [i for i in response.keys()],
                    'Value': [i for i in response.values()]
                })

                # Set the coordinates limits
                upperLimit = 100
                lowerLimit = 30

                # Compute max and min in the dataset
                max = df['Value'].max()

                # Let's compute heights: they are a conversion of each item value in those new coordinates
                # In our example, 0 in the dataset will be converted to the lowerLimit (10)
                # The maximum will be converted to the upperLimit (100)
                slope = (max - lowerLimit) / max
                heights = slope * df.Value + lowerLimit

                # Compute the width of each bar. In total we have 2*Pi = 360°
                width = 2*np.pi / len(df.index)

                # Compute the angle each bar is centered on:
                indexes = list(range(1, len(df.index)+1))
                angles = [element * width for element in indexes]

                # Draw bars
                bars = ax.bar(
                    x=angles,
                    height=heights,
                    width=width,
                    bottom=lowerLimit,
                    linewidth=2,
                    edgecolor="white")

                # little space between the bar and the label
                labelPadding = 4

                # Add labels
                for bar, angle, height, label in zip(bars,angles, heights, df["Name"]):

                    # Labels are rotated. Rotation must be specified in degrees :(
                    rotation = np.rad2deg(angle)

                    # Flip some labels upside down
                    alignment = ""
                    if angle >= np.pi/2 and angle < 3*np.pi/2:
                        alignment = "right"
                        rotation = rotation + 180
                    else:
                        alignment = "left"

                    # Finally add the labels
                    ax.text(
                        x=angle,
                        y=lowerLimit + bar.get_height() + labelPadding,
                        s=label,
                        ha=alignment,
                        va='center',
                        rotation=rotation,
                        rotation_mode="anchor")

                # fig = plt.figure()
                # fig.patch.set_facecolor(f'#{mood_colors[our_mood]}')
                # fig.patch.set_alpha(0.6)
                # ax = fig.add_subplot(111)
                # ax.patch.set_facecolor('white')
                # ax.patch.set_alpha(0.6)
                # ax.tick_params(axis='both', colors='white', labelsize=12)
                # plt.bar(x = response.keys(), height = response.values(), color ='purple')
                # plt.show()
                st.subheader(f'Current Mood: {our_mood.title()}')
                st.pyplot()
                st.markdown(response)
                select_playlist(our_mood)
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
    except:
        # Prevent the error from propagating into your Streamlit app.
        pass
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
