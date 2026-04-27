#importing libraries

import streamlit as st
import os

from dotenv import load_dotenv
from tavily import TavilyClient
from groq import Groq


#loading API Keys

load_dotenv()

TAVILY_API_KEY = st.secrets.get('TAVILY_API_KEY') or os.getenv('TAVILY_API_KEY')
GROQ_API_KEY = st.secrets.get('GROQ_API_KEY') or os.getenv('GROQ_API_KEY')


#initializing groq client

client = Groq(api_key=GROQ_API_KEY)


#setting up the page

st.set_page_config(page_title='Klugekopf TechBridge AI Agent', page_icon='🤖', layout="centered")

#st.title('🤖 Klugekopf TechBridge AI Agent')
#st.subheader('Researcher | Content Creator | SEO Optimizer')

#using html and css to stylr page title and subhead
st.markdown("""
    <style>
    /* Main Background - Clean White to match the site */
    .stApp {
        background-color: #ffffff;
    }
    
    /* Header Container */
    .header-container {
        background-color: #ffffff;
        padding: 25px;
        border-bottom: 1px solid #e6e9ef;
        margin-bottom: 30px;
        text-align: left; /* Aligned left like the logo */
    }
    
    /* The Gradient for 'Klugekopf' */
    .klugekopf-text {
        background: linear-gradient(to right, #40E0D0, #0000FF); /* Teal to Royal Blue */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }

    /* The 'TechBridge' part in Black */
    .techbridge-text {
        color: #000000;
        font-weight: 800;
    }

    .full-title {
        font-size: 32px;
        font-family: 'sans-serif';
    }

    .subtitle {
        color: #000;
        font-size: 18px;
        margin-top: 5px;
        font-weight: 600;
        text-align: center;
    }

    /* Blue Pill Button style to match the site's action buttons */
    div.stButton > button {
        background-color: #0000FF !important;
        color: white !important;
        border-radius: 50px !important;
        padding: 10px 25px !important;
        border: none !important;
        font-weight: bold !important;
    }
    </style>
    
    <div class="header-container">
        <div class="full-title" style="text-align: center;">
            🤖 <span class="klugekopf-text">Klugekopf</span> <span class="techbridge-text">TechBridge</span> AI Agent
        </div>
        <div class="subtitle">Researcher | Content Creator | SEO Optimizer</div>
    </div>
    """, unsafe_allow_html=True)




#adding user topic input prompt

topic = st.text_input('Enter a topic to research and write about:')




#adding button and main logic

if st.button('Generate Content'):
    if topic:
        with st.spinner('Agents are working...'):
             
             #code for running the tavily research

             tavily = TavilyClient(api_key=TAVILY_API_KEY)
             research = tavily.search(query=topic, search_depth='advanced')
             research_text = '\n'.join([r['content'] for r in research['results']])

             
             #tbuilding he agent prompt

             prompt = f"""
             You are a team of 3 AI agents:
             1. Researcher - You have found this information: {research_text}
             2. Content Creator - Write a detailed blog post about: {topic}
             3. SEO Optimizer - Optimize the blog post with keywords, meta description and SEO tips

             Please provide:
             - A full blog post
             - Meta description
             - Recommended keywords
             - SEO tips
             """


             #sending to Groq and displaying the results

             response = client.chat.completions.create(
                model='llama-3.3-70b-versatile',
                messages=[{'role': 'user', 'content': prompt}]
             )
             st.success('Done!')
             #st.markdown('### Generated Content')
             #st.write(response.choices[0].message.content)

             #variavle for storing the results for use in the card html

             final_content = response.choices[0].message.content

             #creating/styling a card to hold the output
        st.markdown(f"""
            <div style="
            background-color: white; 
            padding: 30px; 
            border-radius: 12px; 
            border: 1px solid #e6e9ef; 
            border-left: 10px solid #0000FF;
            box-shadow: 0px 10px 25px rgba(0,0,0,0.15);
            margin-top: 20px;
            ">
            <h4 style="color: #40E0D0; margin: 0 0 10px 0; font-family: sans-serif;">
            📝 GENERATED CONTENT
            </h4>
            <p style="color: #333333; line-height: 1.6; font-family: sans-serif;">
            {final_content}
            </p>
            </div>
        """, unsafe_allow_html=True)

             
    
             


    #Empty topic warning
    
    else:
        st.warning('Please enter a topic first!')
            


