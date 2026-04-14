# Requirement

## Python
- Python 3.10 or newer

## Dependencies
- streamlit
- langchain
- langchain-openai

## Optional Environment Variables
Set these before running:
- MODEL_NAME
- UNIAPI_KEY
- BASE_URL

## Install
```bash
pip install -U streamlit langchain langchain-openai
```

## Run
```bash
streamlit run app.py
```

## Project Structure
- app.py: Streamlit UI
- chain.py: LangChain generation logic
