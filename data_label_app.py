"""
data_label_app.py

This Streamlit application allows the user to visualize and label sensor data. The application takes a CSV file containing sensor 
data as input and displays a plot of the sum of the x, y, and z values. The user can label specific portions of the data by clicking 
buttons corresponding to different labels (e.g., "Still," "Walking," "Jumping"). The labeled dataset can be saved as a CSV file.

Usage:
1. Install the required dependencies: streamlit, pandas, matplotlib.
2. Run the script using a Python interpreter: `streamlit run data_label_app.py`.
3. Enter the path to the sensor data CSV file in the provided text input.
4. Interact with the application by clicking the labeling buttons and providing an output path to save the labeled dataset.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

path = st.text_input('Enter Data Path')

# Check if the path value has changed
if path != st.session_state.get('previous_path', ''):
    # Clear session state data
    st.session_state.clear()

# Update the previous_path session variable
st.session_state.previous_path = path

if path != '':
    # Initialize variables using session state
    if 'start_index' not in st.session_state:
        st.session_state.start_index = 0
    if 'end_index' not in st.session_state:
        st.session_state.end_index = 15
    if 'data' not in st.session_state:
        st.session_state.data = pd.read_csv(path)
        if 'labels' not in st.session_state.data.columns:
            st.session_state.data['labels'] = ''

    # Apply custom CSS
    st.markdown(
        """
        <style>
        .css-19rxjzo {
            width: 100%;
        }

        .css-19rxjzo p {
            font-size: 30px
        }

        .css-tvhsbf {
            width: 100%;
            margin-top: 5%;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Display the plot
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_ylim(-20, 10)
    ax.plot(st.session_state.data.iloc[:, :3].sum(1))
    ax.set_xlabel('x')
    ax.set_ylabel('y')

    # Highlight the data points
    highlighted_data = st.session_state.data.iloc[:, :3].sum(1)[st.session_state.start_index:st.session_state.end_index]
    ax.plot(highlighted_data, color='red')

    # Set the plot layout
    st.pyplot(fig)

    # Add buttons for labeling
    button_col1, button_col2, button_col3 = st.columns(3)
    if button_col1.button('Still', key='still'):
        st.session_state.data.loc[st.session_state.start_index-15+(1 if st.session_state.start_index-15 != 0 else 0):st.session_state.end_index-15, 'labels'] = 'still'

    if button_col2.button('Walking', key='walking'):
        st.session_state.data.loc[st.session_state.start_index-15+(1 if st.session_state.start_index-15 != 0 else 0):st.session_state.end_index-15, 'labels'] = 'walking'

    if button_col3.button('Jumping', key='jumping'):
        st.session_state.data.loc[st.session_state.start_index-15+(1 if st.session_state.start_index-15 != 0 else 0):st.session_state.end_index-15, 'labels'] = 'jumping'

    if st.session_state.start_index > len(st.session_state.data):
        st.markdown('# Data Over!')
    else:
        st.session_state.start_index += 15
        st.session_state.end_index += 15

    # Display the dataset
    st.write(st.session_state.data)

    # save data
    output_path = st.text_input('Output Path')

    if output_path != '':
        st.session_state.data.to_csv(output_path, index=False)
        st.write('Labeled Dataset Saved!')
