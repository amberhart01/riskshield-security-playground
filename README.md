# RiskShield_Project7
Spring Class 2025 MSA8700 Project 7
Members: Christine Simpson, Amber Hart, Eric Brown, Irina Risjuka, Charles Effisah, Zakir Jones​
Team's Miro Board: https://miro.com/app/board/uXjVIDYrqO4=/

🧠 AI-Powered Security Assessment Assistant – Solution Architecture 

✅ Business Problem 

Consultants spend a significant amount of time manually reviewing cybersecurity frameworks like NIST 800-53 or CIS Controls, evaluating client evidence, and compiling lengthy reports. This process is time-consuming, repetitive, and costly. Your AI assistant aims to: 

- Review and interpret controls. 
- Analyze supporting documentation (e.g., policies, screenshots).
- Generate preliminary audit findings and reports. 
- Reduce time-to-delivery and consultant workload. 
 

🏗️ Solution Architecture Overview 

1. User Interface (UI) 

Framework: Streamlit or Flask (easy to deploy and use) 
Features: 
- Upload documents (PDF, DOCX, TXT) 
- Select framework (NIST, CIS, etc.) 
- View AI-generated summaries and findings in dashboard 
- Textbox for control/assessment survey questions and answers 
- Download draft report 
- Email report to consultant/client with results 

2. Backend/LLM Engine 

LLM Provider: OpenAI GPT-4 or Ollama (if self-hosting) 
Features: 
- Prompt chaining for control understanding → document analysis → findings 
- Vector database for context retrieval (using FAISS, ChromaDB, or Pinecone) 
- Optional fine-tuning or function-calling (e.g., report generation in sections) 

3. Document Parser/Preprocessor 

- Use Python libraries (pdfminer, docx, textract) to extract and clean content. 
- Chunk large documents into digestible parts for LLM consumption. 

4. RAG Pipeline (Retrieval-Augmented Generation) 

- Index documents into a vector store. 
- Use embeddings to retrieve the most relevant sections when assessing a control. 
- Pass those to the LLM for analysis and reporting. 

5. Output & Reporting 

- Summarize findings per control (e.g., “Partially Implemented” with rationale). 
- Generate downloadable draft report (PDF or DOCX). 
- Optional: Export as structured JSON for integration into other GRC tools. 

6. Deployment 

- Platform: Streamlit Cloud, Render, Azure Web App, or AWS EC2/S3 
- Access: Publicly accessible URL for classmates to demo 
- Security: Basic authentication if required 
 

📈Diagram 
 

https://www.mermaidchart.com/app/projects/aa87f806-3788-4a4f-8255-81980208820d/diagrams/54eaf0b6-0176-43ff-ab69-a5831c2e9375/version/v0.1/edit 

 

 Mock page: https://chatgpt.com/canvas/shared/67e0aba6fc3881918209ff8ae4a07566
 Web Design page help: https://chatgpt.com/share/67e0abcf-01d8-800e-96cf-533108ffc5db

test change
