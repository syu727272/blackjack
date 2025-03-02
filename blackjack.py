#!/usr/bin/env -S python -m streamlit run 

import streamlit as st
import bj

class State:
    def __init__(self):
        self.state = 'play'                # play, bust, or showdown
        self.deck = bj.Deck()
        self.player = bj.Player(self.deck)


if 'state' not in st.session_state:
    st.session_state.state = State()

state = st.session_state.state

container_dealer = st.container(border=True)
container_dealer.markdown('**Dealer**')

container_player = st.container(border=True)
container_player.markdown('**Player**')

if state.state == 'play':
    with st.sidebar:
        if st.button('カードを引く'):
            state.player.draw()
            if state.player.score is None:
                state.state = 'bust'
                st.rerun()

        if st.button('勝負する'):
            state.state = 'showdown'
            st.rerun()

    container_dealer.html(bj.back_cards())
    container_player.html(state.player.show_html())

elif state.state == 'bust':
    with st.sidebar:
        if st.button('再勝負?'):
            del st.session_state.state
            st.rerun()

    container_dealer.html(bj.back_cards())
    container_player.html(state.player.show_html())
    container_player.markdown(f'どぼん')

else:
    with st.sidebar:
        if st.button('再勝負?'):
            del st.session_state.state
            st.rerun()

    dealer = bj.Player(state.deck)
    dealer.auto_draw()
    message = state.player.showdown(dealer)

    container_dealer.html(dealer.show_html())
    container_player.html(state.player.show_html())
    container_player.markdown(f'**{message}**')
    if message == '勝ち':
        st.balloons()
