Agentic AI

1.  ## Financial AI analyst
    - financial_agent.py: A Python-based AI agent system using the Phi framework   for financial analysis and web searches.
    - playground.py: the interactive UI within the Phidata platform.  First, run "python playground.py", Then login to your Phidata console, navigate to Playgound, connect to the localhost:7777, it load the agent you built from your local env.  See the phidata-playground.jpg snapshot.

    ### Features
    - Financial AI Agent: Analyzes stock data using YFinance
    - Web Search Agent: Performs web searches using DuckDuckGo
    - Multi AI Agent: Combines both agents for comprehensive analysis

2.  ## Pdf Assistant
    - pdf_assistant.py:  A Python-based document analysis system using the Phi framework for processing and querying PDF content
  
    ### Features
    - PDF Knowledge Base: Ingests and vectorizes PDF documents using PDFUrlKnowledgeBase
    - Persistent Storage: Maintains chat history and document embeddings in PostgreSQL
    - Vector Search: Uses pgvector for semantic document search
    - Interactive CLI: Provides markdown-supported conversational interface
