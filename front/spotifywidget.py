import streamlit as st
import streamlit.components.v1 as components

def select_and_play(feeling):
    happiness = 'https://open.spotify.com/playlist/556ICk4gRzDknRfWGeQ3x1'
    sadness = 'https://open.spotify.com/playlist/0dRxDrR1PfZMlVbfnuBRbR'
    anger = 'https://open.spotify.com/embed/playlist/7FjP7MbRgFYFdv5avuhiBI'
    enthusiasm = 'https://open.spotify.com/playlist/4JsAKbWk4AoBcfpSs2afOM'
    empty = 'https://open.spotify.com/playlist/77OpFLSdLy3nC9huQIXlxk'
    boredom = 'https://open.spotify.com/playlist/2rA0wLILuvNuLhAacn4kth'
    worry = 'https://open.spotify.com/playlist/5Dt93qIXccZvZbU6r3oIbs'
    love = 'https://open.spotify.com/playlist/73KuPUAtOecLDAetRn80TW'
    surprise = 'https://open.spotify.com/playlist/0BaRZECQEqp4zDd0Njzlj1'
    fun = 'https://open.spotify.com/playlist/7HwdXmzNKXBzTAisOKYVsJ'
    relief = 'https://open.spotify.com/playlist/2zaAFRdI6lEaX8Esc11XPZ'
    hate = 'https://open.spotify.com/playlist/6vdOF3ZRqiYimqEm4lk98V'
    neutral = 'https://open.spotify.com/playlist/5pSdjjPHbXpbqFJGf31Ksn'

<iframe src="https://open.spotify.com/embed/playlist/7FjP7MbRgFYFdv5avuhiBI" width="300" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>


    d= {'happiness':happiness, 'sadness':sadness, 'worry':worry, 'love':love, 
        'anger':anger, 'fun':fun, 'relief': relief, 'empty':empty,
        'hate':hate, 'enthusiasm':enthusiasm, 'surprise':surprise,
        'boredom':boredom, 'neutral':neutral
       }
    
    mood = d[feeling]

    return components.html(
        f"""
        <iframe src={mood} width="100%" height="380" frameBorder="0" allowtransparency="true" allow="encrypted-media"></iframe>
        """,
        height=200,
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