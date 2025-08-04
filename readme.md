# TechStack Used

Gemini LLM model
MongoDB
Python
FastAPI


# Problem Statement 

Businesses receive huge amounts of information in different formats (emails, PDFs, JSON from APIs), and humans currently waste time reading, sorting, and manually entering this data into internal systems.

# We are automating :
1. Data intake
2. Intent understanding
3. Contextual memory across interactions
4. Routing to the right processing logic

# Key benefits :
1. Massive time saving 
2. Reduces human error
3. Scales up businesses
4. Supports automation and Integration

# Project Workflow : 

1. Input Received
The system receives raw data in PDF, JSON, or Email format — without knowing the type or intent.

2. Classifier Agent

Detects the format (e.g., email, json)

Identifies the intent (e.g., RFQ, invoice, complaint).

Intents for our MVP are :
     a. RFQ
     b. Order PLacement
     c. Invoice
     d. Complaint

3. Specialized Agents

a. JSON Agent
Accepts any JSON payload

Based on the intent, selects the correct internal schema

Extracts, validates, and checks for missing fields

Saves the structured output to Mongo DB for downstream use

b. Email Parser Agent

Processes the email body

Extracts metadata like sender name, urgency, company

Generates a conversation/thread ID

Stores all parsed info into Mongo DB

c. pdfAgent 

Processes the pdf body

Extracts metadata like sender name, urgency, company

Generates a conversation/thread ID

Stores all parsed info into Mongo DB

# Shared Memory (Mongo DB)

Central context store shared across all agents

Tracks input metadata, extracted fields, and conversation history

Ensures continuity if inputs are linked (e.g., email + JSON)

# Chaining & Final Output

If one input references another (e.g., email links a JSON), it’s routed accordingly

Final structured data is ready for use in CRMs, audits, or automation systems

# Conclusion :

It bridges the gap beWeen messy real-world inputs and clean, structured, useful data.
It helps organizations move faster, smarter, and more efficiently while reducing cost and error.