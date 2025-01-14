from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
import io
import sys
import re

app = FastAPI()

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

def clean_output(output):
    # Remove ANSI escape sequences
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', output)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head>
            <title>Financial Agent</title>
        </head>
        <body>
            <h1>Welcome to the Financial Agent</h1>
            <form action="/analyze" method="get">
                <label for="ticker">Enter stock ticker symbol:</label>
                <input type="text" id="ticker" name="ticker" required>
                <input type="submit" value="Analyze">
            </form>
        </body>
    </html>
    """

@app.get("/analyze", response_class=HTMLResponse)
async def analyze(ticker: str):
    multi_ai_agent = create_agents()
    try:
        query = f"Summarize analyst recommendation and share the latest news for {ticker.upper()}"
        
        # Redirect stdout to capture print_response output
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        
        # Call the print_response method
        multi_ai_agent.print_response(query, stream=False)
        
        # Reset stdout
        sys.stdout = old_stdout
        
        # Get the captured output
        raw_response = new_stdout.getvalue()
        
        # Clean the output
        response = clean_output(raw_response)
        
        return f"""
        <html>
            <head>
                <title>Analysis for {ticker.upper()}</title>
            </head>
            <body>
                <h1>Analysis for {ticker.upper()}</h1>
                <pre>{response}</pre>
                <a href="/">Back</a>
            </body>
        </html>
        """
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)