from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo

from dotenv import load_dotenv
load_dotenv()

def create_agents():
    # Web search agent
    web_search_agent = Agent(
        name="Web Search Agent",
        role="Search the web for the information",
        model=Groq(id="llama-3.3-70b-versatile"),
        tools=[DuckDuckGo()],
        instructions=["Always include sources"],
        show_tool_calls=True,
        markdown=True,
    )

    # Financial agent
    financial_agent = Agent(
        name="Finance AI Agent",
        model=Groq(id="llama-3.3-70b-versatile"),
        tools=[
            YFinanceTools(stock_price=True, analyst_recommendations=True, 
                         stock_fundamentals=True, company_news=True)
        ],
        instructions=["Use tables to display the data"],
        show_tool_calls=True,
        markdown=True
    )

    # Multi AI agent
    multi_ai_agent = Agent(
        model=Groq(id="llama-3.1-70b-versatile"),
        team=[web_search_agent, financial_agent],
        instructions=["Always include sources", "use table to display the data"],
        show_tool_calls=True,
        markdown=True
    )
    
    return multi_ai_agent

def main():
    # Create agents
    multi_ai_agent = create_agents()
    
    while True:
        # Get user input
        ticker = input("\nEnter stock ticker symbol (or 'quit' to exit): ").strip().upper()
        
        if ticker.lower() == 'quit':
            print("Exiting program...")
            break
            
        if not ticker:
            print("Please enter a valid ticker symbol")
            continue
            
        try:
            # Generate the query
            query = f"Summarize analyst recommendation and share the latest news for {ticker}"
            print(f"\nAnalyzing {ticker}...")
            
            # Get response
            multi_ai_agent.print_response(query, stream=True)
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print("Please try again with a different ticker symbol")

if __name__ == "__main__":
    main()