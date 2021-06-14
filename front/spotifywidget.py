import streamlit as st
import streamlit.components.v1 as components

def select_and_play(feeling):
    happiness = 'https://open.spotify.com/embed/playlist/556ICk4gRzDknRfWGeQ3x1'
    sadness = 'https://open.spotify.com/embed/playlist/0dRxDrR1PfZMlVbfnuBRbR'
    anger = 'https://open.spotify.com/embed/playlist/7FjP7MbRgFYFdv5avuhiBI'
    fear = 'https://open.spotify.com/embed/playlist/6EF56fuiUgN2GOMVZIiXpq'
    love = 'https://open.spotify.com/embed/playlist/73KuPUAtOecLDAetRn80TW'
    neutral = 'https://open.spotify.com/embed/playlist/5pSdjjPHbXpbqFJGf31Ksn'


    d= {'happiness':happiness, 'sadness':sadness, 'love':love, 
        'anger':anger, 'neutral':neutral
       }
    
    mood = d[feeling]

    return components.html(
        f"""
        <iframe src={mood} width="100%" height="380" frameBorder="0" allowtransparency="true" allow="encrypted-media"></iframe>
        """,
        height=800,
    )


# def select_link(mood):
#     return components.html(
#             f'''
#                 <iframe src="{mood}" width="300" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
#             ''',
#             height=600
#         )
    

# components.html(
#     '''
#         <iframe src="https://spotify.com/embed/playlist/7xOHp3ZlSBJNJOgsQwF85S" width="300" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
#     ''',
#     height=600
# )


def music_player(input):
  components.html(
    f"""
    <iframe src={input} width="100%" height="380" frameBorder="0" allowtransparency="true" allow="encrypted-media"></iframe>
    """,
    height=200,
  )