# twitter_post_app.py
import streamlit as st
import tweepy
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twitter API configuration
def twitter_auth():
    try:
        consumer_key = os.getenv("CONSUMER_KEY")
        consumer_secret = os.getenv("CONSUMER_SECRET")
        access_token = os.getenv("ACCESS_TOKEN")
        access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
        
        client = tweepy.Client(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )
        return client
    except Exception as e:
        st.error(f"Authentication failed: {str(e)}")
        return None

# Streamlit app
st.title("🚀 Twitter Post App")
st.markdown("Post tweets directly to your Twitter account")

# Initialize session state
if 'tweet_posted' not in st.session_state:
    st.session_state.tweet_posted = False

# Sidebar for credentials management
with st.sidebar:
    st.subheader("Twitter API Credentials")
    use_custom_creds = st.checkbox("Use custom credentials")
    
    if use_custom_creds:
        consumer_key = st.text_input("Consumer Key", type="password")
        consumer_secret = st.text_input("Consumer Secret", type="password")
        access_token = st.text_input("Access Token", type="password")
        access_token_secret = st.text_input("Access Token Secret", type="password")
    else:
        consumer_key = os.getenv("CONSUMER_KEY")
        consumer_secret = os.getenv("CONSUMER_SECRET")
        access_token = os.getenv("ACCESS_TOKEN")
        access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

# Main tweet composition area
tweet_text = st.text_area(
    "Compose your tweet", 
    height=150,
    placeholder="What's happening?",
    max_chars=280
)

char_count = len(tweet_text or "")
st.caption(f"{char_count}/280 characters")

col1, col2 = st.columns(2)
with col1:
    include_media = st.checkbox("Include media?")
    
uploaded_file = None
if include_media:
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# Tweet posting functionality
if st.button("Post Tweet"):
    client = None
    try:
        if use_custom_creds:
            client = tweepy.Client(
                consumer_key=consumer_key,
                consumer_secret=consumer_secret,
                access_token=access_token,
                access_token_secret=access_token_secret
            )
        else:
            client = twitter_auth()
        
        if client:
            # Handle media upload
            media_id = None
            if include_media and uploaded_file is not None:
                auth = tweepy.OAuth1UserHandler(
                    consumer_key, consumer_secret,
                    access_token, access_token_secret
                )
                api = tweepy.API(auth)
                media = api.media_upload(filename="uploaded_media", file=uploaded_file)
                media_id = media.media_id
            
            # Post tweet
            response = client.create_tweet(
                text=tweet_text,
                media_ids=[media_id] if media_id else None
            )
            
            st.success("✅ Tweet posted successfully!")
            st.session_state.tweet_posted = True
            st.balloons()
            
            # Show tweet details
            st.subheader("Posted Tweet Details")
            st.code(f"Tweet ID: {response.data['id']}")
            st.code(f"Text: {tweet_text}")
            
        else:
            st.error("Twitter authentication failed")
    
    except tweepy.TweepyException as e:
        st.error(f"Twitter API error: {str(e)}")
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Display success message after posting
if st.session_state.tweet_posted:
    st.info("Refresh the page to post another tweet")