import streamlit as st


def replace_favicon():
    st.set_page_config(
        page_title="Data Manager",
        page_icon="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTibj3To3sNDkYUB-DQyn2Hcu6icV5spAH40A79GyXk9bdZ4vJ23g4nu4xKsG9J7gybQQ&usqp=CAU",
        layout="centered",
        initial_sidebar_state="auto",
    )


def hide_hamburger():
    st.markdown(
        """
    <style>
        .css-1a1tcp.e1ewe7hr3

        {
            visibility : hidden;
        }
        .css-h5rgaw.e1g8pov61
        {
            visibility : hidden;
        }
    </style>

    """,
        unsafe_allow_html=True,
    )


def add_logo():
    st.markdown(
        """
    <!DOCTYPE html>
    <html>
    <head>
    <style>

    .container {
    position: absolute;
    top: -45px;
    left: -380px;
    }
    </style>
    </head>
    <body>

    <div class="container">
    <img src= "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTibj3To3sNDkYUB-DQyn2Hcu6icV5spAH40A79GyXk9bdZ4vJ23g4nu4xKsG9J7gybQQ&usqp=CAU" width="70" height="80">

    </div>

    </body>
    </html>
    """,
        unsafe_allow_html=True,
    )
