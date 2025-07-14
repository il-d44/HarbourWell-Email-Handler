# HarbourWell Email Handler

This project is a prototype email handling system designed for a fictitious mental health organisation called HarbourWell, based in Hertfordshire. It leverages Gemini AI to automate the categorisation, information retrieval, and drafting of email responses for routine enquiries. The system includes a lightweight user interface that facilitates human review before sending.

The prototype uses a Retrieval-Augmented Generation (RAG) approach, where mock data on Harbourwell’s locations and services is chunked and embedded into a vector database. This knowledge base enables the system to efficiently retrieve relevant information, which is then used to generate accurate draft responses to service user enquiries.


## Inspiration
The idea for this project stems from my experience working in communications for mental health services. In dealing with administrative tasks, I often encountered routine email enquiries about services where relevant information was publicly available but not always easily accessible to users.

The goal of this application is to harness AI technology to reduce administrative burdens on staff while providing service users with accurate, timely, and clear information.

## Screenshot of UI

![Inbox view of the Email Handling System](images/ui_screenshot_1.png)


## Disclaimer 

This project is inspired by real-world experiences but is not affiliated with or representative of any mental health organisation. It is intended solely as a programming learning exercise and an experimental exploration of AI for automating business processes. This prototype is for experimental purposes only. The author acknowledges and takes seriously the ethical considerations and potential implications of using AI in the mental health field.



## Features

- Integration with Gmail inbox using the Gmail API to retrieve unread emails

- Classify emails into categories such as "routine enquiry" or "referrals"

- Use a Retrieval-Augmented Generation (RAG) system with embedded mock data and FAISS vector search to retrieve relevant information chunks

- Draft warm, professional email responses with a language model

- Simple Streamlit interface for reviewing and approving responses


## Technical Overview

This prototype follows a modular architecture using class-based agents to handle each stage of the email response pipeline. The key components include:

- InboxAgent: Fetches unread emails via the Gmail API.

- ClassifyAgent: Uses a language model (Gemini) to categorise incoming emails into predefined types.

- RAGAgent: Implements a basic Retrieval-Augmented Generation (RAG) system. It retrieves relevant context from a FAISS-powered vector store of embedded service data.

- DraftResponseAgent: Uses the language model to generate a draft reply based on the email content and retrieved context.

- Each agent is implemented as a standalone Python class, allowing the system to be extended or tested independently.

- The Streamlit app acts as a lightweight user interface and calls the run_supervisor_step function during each interaction. This function coordinates the logic — classification, retrieval, and drafting — depending on the current status in the pipeline.

- st.session_state is used to persist the current email index and the shared Global_State object between interactions, ensuring continuity across user actions (e.g., reviewing and approving draft responses).



## Setup
1. ### Clone the repository

2. ### Install dependencies:
Make sure you have Python 3.10+ and install required packages:

``` pip install -r requirements.txt ``` 

3. ### Authorise Gmail API (opens a browser window for OAuth)
``` python setup/gmail_api_setup.py ```

4. ### 4. Set up Gemini API key
Create a .env file and add your API key:

``` GEMINI_API_KEY=your-key-here ```

5. ### Run the Streamlit app
``` streamlit run pipeline/app.py ```


## Future Improvements
- Support for additional email categories

- Add unit tests and CI/CD integration

- Strengthen guardrails 





## Contact
Created by Ilyaas – feel free to reach out at [ilyaas.daar@gmail.com].