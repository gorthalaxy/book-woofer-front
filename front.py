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
import numpy as np


# f = f'''<style>.myDiv {{border: 5px double DarkOliveGreen;background-color: Cornsilk; text-align: center; padding: 20px;}}</style></head><body><div class="myDiv"><p style="color:Black; text-align:left">hello</p></div>'''



#   Head
#----------------------------------------



st.set_page_config(page_title='Book Woofer',page_icon = 'favicon.png', layout = 'wide')
st.title('Book Woofer')

mood_colors = {'anger': 'E74C3C', 
               'fear': 'D6DBDF' , 
               'happy': 'F1C40F', 
               'love': 'BB8FCE', 
               'neutral': '93E6B4', 
               'sadness': '5DADE2'}

# mood_colors = {'anger': '7B241C', 'fear': '212F3C', 'happy': 'AF601A', 'love': '5B2C6F', 'neutral': '4D5656', 'sadness': '154360'}
make_choice = st.sidebar.selectbox('', ['Upload Ebook', 'Select Ebook', 'Upload Text'])
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
            uploaded_file = st.file_uploader("Upload your ebook:")
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
        #====================Send request and print prediction
                    texts = {'text': out}
                    url = "https://bfcontainer-csy3ocxwaq-ew.a.run.app/predict/"
                    response = requests.post(
                        url,
                        params=texts,
                    ).json()
                    st.markdown("<a href='#linkto_top' style='color:#FFFFFF'>Choose next chapter</a>", unsafe_allow_html=True)
                our_mood = max(response, key=response.get)
                st.set_option('deprecation.showPyplotGlobalUse', False)
                # sidebar_css = """<style>.sidebar .sidebar-content {background-image: linear-gradient(#FFFFFF,#FFFFFF);color: white;}</style>"""
                # st.markdown(sidebar_css,unsafe_allow_html=True)
                
                with st.sidebar:
                    df = pd.DataFrame({
                    'group': ['A'],
                    'anger': [response['anger']],
                    'fear': [response['fear']],
                    'happy': [response['happy']],
                    'love': [response['love']],
                    'neutral': [response['neutral']],
                    'sadness': [response['sadness']]
                    })
                    
                    max_val = np.max(np.array(list(response.values())))
                    
                    # number of variable
                    categories=list(df)[1:]
                    N = len(categories)
                    
                    # We are going to plot the first line of the data frame.
                    # But we need to repeat the first value to close the circular graph:
                    values=df.loc[0].drop('group').values.flatten().tolist()
                    values += values[:1]
                    
                    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
                    angles = [n / float(N) * 2 * np.pi for n in range(N)]
                    angles += angles[:1]
                    
                    # Initialise the spider plot
                    plt.figure(facecolor='#31333F', edgecolor='white')
                    ax = plt.subplot(111, polar=True)
                    
                    # Draw one axe per variable + add labels
                    plt.xticks(angles[:-1], categories, color='white', size=12)
                    
                    # Draw ylabels
                    ax.set_rlabel_position(0)
                    plt.yticks([max_val/4,max_val/4*2,max_val*3/4], [f'{round(max_val/4,2)}',f'{round(max_val*2/4,2)}',f'{round(max_val*3/4, 2)}'], color="white", size=7)
                    plt.ylim(0,max_val)
                    
                    # Plot data
                    ax.plot(angles, values, linewidth=1, color= f'#{mood_colors[our_mood]}' , linestyle='solid')
                    
                    
                    # Fill area
                    ax.fill(angles, values, f'#{mood_colors[our_mood]}', alpha=0.6)
                    ax.spines[:].set_color('white')
                    ax.tick_params(axis='x', grid_color='white')
                    ax.tick_params(axis='y', grid_color='white')
                    ax.set_facecolor('#31333F')
                    # Show the graph
                    # plt.show()
                    # fig = plt.figure()
                    # fig.patch.set_facecolor(f'#{mood_colors[our_mood]}')
                    # fig.patch.set_alpha(1)#0.6)
                    # ax = fig.add_subplot(111)
                    # ax.patch.set_facecolor('white')
                    # ax.patch.set_alpha(1)#0.6)
                    # ax.tick_params(axis='both', colors='black', labelsize=12)
                    # plt.bar(x = response.keys(), height = response.values(), color = f'#{mood_colors[our_mood]}')
                    st.markdown(f"<h3 style='text-align: center;'>Current Mood: {our_mood.title()}</h1>", unsafe_allow_html=True)
                    st.pyplot()
                    
                    select_playlist(our_mood)
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
                    df = pd.DataFrame({
                    'group': ['A'],
                    'anger': [response['anger']],
                    'fear': [response['fear']],
                    'happy': [response['happy']],
                    'love': [response['love']],
                    'neutral': [response['neutral']],
                    'sadness': [response['sadness']]
                    })
                    
                    max_val = np.max(np.array(list(response.values())))
                    
                    # number of variable
                    categories=list(df)[1:]
                    N = len(categories)
                    
                    # We are going to plot the first line of the data frame.
                    # But we need to repeat the first value to close the circular graph:
                    values=df.loc[0].drop('group').values.flatten().tolist()
                    values += values[:1]
                    
                    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
                    angles = [n / float(N) * 2 * np.pi for n in range(N)]
                    angles += angles[:1]
                    
                    # Initialise the spider plot
                    plt.figure(facecolor='#31333F', edgecolor='white')
                    ax = plt.subplot(111, polar=True)
                    
                    # Draw one axe per variable + add labels
                    plt.xticks(angles[:-1], categories, color='white', size=12)
                    
                    # Draw ylabels
                    ax.set_rlabel_position(0)
                    plt.yticks([max_val/4,max_val/4*2,max_val*3/4], [f'{round(max_val/4,2)}',f'{round(max_val*2/4,2)}',f'{round(max_val*3/4, 2)}'], color="white", size=7)
                    plt.ylim(0,max_val)
                    
                    # Plot data
                    ax.plot(angles, values, linewidth=1, color= f'#{mood_colors[our_mood]}' , linestyle='solid')
                    
                    
                    # Fill area
                    ax.fill(angles, values, f'#{mood_colors[our_mood]}', alpha=0.6)
                    ax.spines[:].set_color('white')
                    ax.tick_params(axis='x', grid_color='white')
                    ax.tick_params(axis='y', grid_color='white')
                    ax.set_facecolor('#31333F')
                    # Show the graph
                    # plt.show()
                    # fig = plt.figure()
                    # fig.patch.set_facecolor(f'#{mood_colors[our_mood]}')
                    # fig.patch.set_alpha(1)#0.6)
                    # ax = fig.add_subplot(111)
                    # ax.patch.set_facecolor('white')
                    # ax.patch.set_alpha(1)#0.6)
                    # ax.tick_params(axis='both', colors='black', labelsize=12)
                    # plt.bar(x = response.keys(), height = response.values(), color = f'#{mood_colors[our_mood]}')
                    st.markdown(f"<h3 style='text-align: center;'>Current Mood: {our_mood.title()}</h1>", unsafe_allow_html=True)
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
    book_choice = st.selectbox('Pick an ebook to read:', ['Alices Adventures in Wonderland', 'The White Feather', 'King of Terror'])
    st.markdown("<div id='linkto_top'></div>", unsafe_allow_html=True)
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
    st.markdown("<a href='#linkto_top' style='color:#FFFFFF'>Choose next chapter</a>", unsafe_allow_html=True)
    our_mood = max(response, key=response.get)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    with st.sidebar:
        df = pd.DataFrame({
        'group': ['A'],
        'anger': [response['anger']],
        'fear': [response['fear']],
        'happy': [response['happy']],
        'love': [response['love']],
        'neutral': [response['neutral']],
        'sadness': [response['sadness']]
        })
        
        max_val = np.max(np.array(list(response.values())))
        
        # number of variable
        categories=list(df)[1:]
        N = len(categories)
        
        # We are going to plot the first line of the data frame.
        # But we need to repeat the first value to close the circular graph:
        values=df.loc[0].drop('group').values.flatten().tolist()
        values += values[:1]
        
        # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]
        
        # Initialise the spider plot
        plt.figure(facecolor='#31333F', edgecolor='white')
        ax = plt.subplot(111, polar=True)
        
        # Draw one axe per variable + add labels
        plt.xticks(angles[:-1], categories, color='white', size=12)
        
        # Draw ylabels
        ax.set_rlabel_position(0)
        plt.yticks([max_val/4,max_val/4*2,max_val*3/4], [f'{round(max_val/4,2)}',f'{round(max_val*2/4,2)}',f'{round(max_val*3/4, 2)}'], color="white", size=7)
        plt.ylim(0,max_val)
        
        # Plot data
        ax.plot(angles, values, linewidth=1, color= f'#{mood_colors[our_mood]}' , linestyle='solid')
        
        
        # Fill area
        ax.fill(angles, values, f'#{mood_colors[our_mood]}', alpha=0.6)
        ax.spines[:].set_color('white')
        ax.tick_params(axis='x', grid_color='white')
        ax.tick_params(axis='y', grid_color='white')
        ax.set_facecolor('#31333F')
        # Show the graph
        # plt.show()
        # fig = plt.figure()
        # fig.patch.set_facecolor(f'#{mood_colors[our_mood]}')
        # fig.patch.set_alpha(1)#0.6)
        # ax = fig.add_subplot(111)
        # ax.patch.set_facecolor('white')
        # ax.patch.set_alpha(1)#0.6)
        # ax.tick_params(axis='both', colors='black', labelsize=12)
        # plt.bar(x = response.keys(), height = response.values(), color = f'#{mood_colors[our_mood]}')
        st.markdown(f"<h3 style='text-align: center;'>Current Mood: {our_mood.title()}</h1>", unsafe_allow_html=True)
        st.pyplot()
        select_playlist(our_mood)