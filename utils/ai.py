import ollama

def analyze_question(query):
    """Identifies the type of question and extracts the key aspects"""
    question_types = {
        'price': ['price', 'cost', 'how much', 'value', 'worth'],
        'news': ['news', 'update', 'latest', 'happening', 'recent'],
        'market': ['market cap', 'ranking', 'rank', 'position', 'compare'],
        'technical': ['technical', 'analysis', 'chart', 'indicator', 'trend'],
        'future': ['prediction', 'forecast', 'outlook', 'future', 'expect'],
        'general': ['tell me about', 'what is', 'explain', 'who', 'when']
    }
    
    query_lower = query.lower()
    for q_type, keywords in question_types.items():
        if any(keyword in query_lower for keyword in keywords):
            return q_type
    return 'general'

def generate_response(query, news, price, market_data):
    q_type = analyze_question(query)
    
    prompt = f"""
    You are an expert cryptocurrency analyst. Provide a detailed, analytical response to the following question:
    
    Question: "{query}"
    
    Available data:
    - Current Price: ${price:,.2f}
    - Market Cap: ${market_data['market_cap']:,.0f}
    - Rank: #{market_data['rank']}
    - 24h Change: {market_data['price_change_24h']}%
    - Latest News: {[f"{n['title']} ({n['published']})" for n in news]}
    
    Guidelines for your response:
    1. Directly address the specific question asked
    2. Provide concrete analysis using the available data
    3. For price-related questions, include historical context and volatility analysis
    4. For news questions, highlight the most significant developments and their potential impact
    5. For market questions, compare with competitors and analyze positioning
    6. Include specific numbers and metrics when available
    7. Maintain a professional but accessible tone
    8. If the question is speculative, clearly distinguish between facts and projections
    
    Structure your response in 3-5 concise but information-rich sentences.
    """
    
    try:
        response = ollama.chat(
            model='llama2',
            messages=[{'role': 'user', 'content': prompt}],
            options={'temperature': 0.5}  
        )
        return response['message']['content']
    except Exception as e:
        return f"AI Error: {str(e)}"
