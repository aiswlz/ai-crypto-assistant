import streamlit as st
from utils.news import get_crypto_news
from utils.exchange import get_crypto_price
from utils.market import get_market_data, get_top_coins
from utils.ai import generate_response
from dotenv import load_dotenv
from datetime import datetime
import webbrowser

load_dotenv()

st.set_page_config(
    page_title="Advanced Crypto Assistant",
    page_icon="",
    layout="wide"
)

st.markdown("""
<style>
.news-card {
    padding: 20px;
    border-radius: 10px;
    margin: 15px 0;
    border-left: 4px solid #6a5acd;
    background-color: #f8f9fa;
}
.news-title {
    font-weight: 600;
    font-size: 1.2em;
    color: #2c3e50;
    margin-bottom: 8px;
}
.news-meta {
    color: #7f8c8d;
    font-size: 0.9em;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
}
.news-source {
    background-color: #e0e0e0;
    padding: 2px 8px;
    border-radius: 4px;
    margin-right: 10px;
}
.news-date {
    display: flex;
    align-items: center;
}
.news-link {
    color: #6a5acd !important;
    text-decoration: none !important;
    font-weight: 500;
    display: inline-flex;
    align-items: center;
}
.news-link:hover {
    text-decoration: underline !important;
}
</style>
""", unsafe_allow_html=True)

def open_url(url):
    webbrowser.open_new_tab(url)

def display_news(news_items):
    for item in news_items:
        with st.container():
            st.markdown(f"""
            <div class="news-card">
                <div class="news-title">{item['title']}</div>
                <div class="news-meta">
                    <span class="news-source">{item['source']}</span>
                    <span class="news-date">🕒 {item['published']}</span>
                </div>
                <p>{item['excerpt'] if item['excerpt'] != 'No description available' else 'No additional details available'}</p>
                <a href="{item['url']}" target="_blank" class="news-link">
                    Read full story →
                </a>
            </div>
            """, unsafe_allow_html=True)

def main():
    st.title("Advanced Crypto Assistant")
    
    if 'current_coin' not in st.session_state:
        st.session_state.current_coin = None
    
    top_coins = get_top_coins()
    
    coin_symbol = st.selectbox(
        "Select cryptocurrency:",
        list(top_coins.keys()),
        key='coin_select'
    )
    coin_id = top_coins[coin_symbol]
    
    query = st.text_input(
        "Ask any crypto question:",
        value=f"What's happening with {coin_symbol}?",
        key='query_input'
    )
    
    if st.button("Analyze", type="primary"):
        with st.spinner("Gathering and analyzing data..."):
            news = get_crypto_news(coin_symbol)
            price = get_crypto_price(coin_symbol)
            market_data = get_market_data(coin_id)
            answer = generate_response(query, news, price, market_data)
            
            st.session_state.current_coin = {
                'symbol': coin_symbol,
                'answer': answer,
                'news': news,
                'price': price,
                'market_data': market_data,
                'query': query,
                'time': datetime.now().strftime("%H:%M:%S")
            }
    
    if st.session_state.current_coin and st.session_state.current_coin['symbol'] == coin_symbol:
        data = st.session_state.current_coin
        
        st.markdown("---")
        st.subheader("Analysis Result")
        st.markdown(f"**Question:** {data['query']}")
        st.success(data['answer'])
        st.caption(f"Last updated at: {data['time']} UTC")
        
        st.markdown("---")
        st.subheader(f"Latest {data['symbol']} Developments")
        display_news(data['news'])
        
        st.markdown("---")
        st.subheader("Market Snapshot")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Current Price", f"${data['price']:,.2f}")
        with col2:
            st.metric("Market Cap", f"${data['market_data']['market_cap']:,.0f}")
        with col3:
            st.metric("Rank", f"#{data['market_data']['rank']}")
        with col4:
            st.metric("24h Change", f"{data['market_data']['price_change_24h']}%")

if __name__ == "__main__":
    main()