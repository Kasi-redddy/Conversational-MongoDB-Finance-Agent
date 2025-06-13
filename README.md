# 💬 Conversational MongoDB Finance Agent

A robust, context-aware Conversational Database Agent that answers natural language questions about finance data stored in MongoDB — using Retrieval Augmented Generation (RAG) and LLaMA 3 (via Ollama) for query translation.

---

## 🚀 Features

- **Ask Anything**: Definitions, filters, aggregations, trends, comparisons, and more.
- **True RAG**: Answers generated from your real MongoDB data using LLaMA 3 for NL → MongoDB query translation.
- **Multi-Collection Support**: Handles `accounts`, `customers`, and `transactions`.
- **Contextual Conversation**: Maintains memory for follow-up and multi-turn interactions.
- **Robust Error Handling**: Flags ambiguous/impossible queries and provides actionable feedback.
- **Clean UI**: Simple Streamlit interface for interactive querying and demos.

---

## 🏗️ Architecture

```
User (Natural Language Query)
        ↓
   Streamlit UI
        ↓
Conversational Agent (Python)
        ↓
  LLaMA 3 (Ollama)
        ↓
MongoDB Atlas (sample_analytics)
        ↓
     Results
```

- **UI**: Streamlit Web App  
- **Agent**: Python backend with context memory, RAG logic, and fallback system  
- **LLM**: LLaMA 3 (via Ollama)  
- **Database**: MongoDB Atlas → `sample_analytics` (Finance Dataset)

---

## 🛠️ Setup Instructions

1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/conversational-mongodb-finance-agent.git
cd conversational-mongodb-finance-agent
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure MongoDB Atlas**
- Uses the free **sample_analytics** dataset.
- If using your own cluster, update `MONGODB_URI` in `db.py`.

4. **Start Ollama with LLaMA 3**
```bash
ollama run llama3
```
> Download Ollama and the LLaMA 3 model if not installed already.

5. **Run the App**
```bash
streamlit run app.py
```

---

## 🧑‍💻 Usage

Open your browser and use the Streamlit interface to ask questions like:

- "Show all customers."
- "What is the address of Elizabeth Ray?"
- "List transactions over $1000."
- "Which account has the highest limit?"
- "Show me all products associated with account_id 371138."
- "Give me the email for username fmiller."
- "Who owns account_id 443178?"
- "Show the total number of transactions per customer."
- "Show all transactions for customer Elizabeth Ray."

---

## 🧪 Example Test Questions

- Show all customers.  
- What is the address of Elizabeth Ray?  
- List transactions over $1000.  
- Show customers with `active` status `true`.  
- Find accounts with a limit greater than 5000.  
- What is the total number of transactions per customer?  
- Show the average transaction amount by account tier.  
- Compare transaction counts between Elizabeth Ray and fmiller.  
- List all products associated with account_id 371138.  
- Who owns account_id 443178?  
- Give details for "dustin37@yahoo.com".  

---

## 📁 Dataset

- **Database**: MongoDB Atlas  
- **Sample**: `sample_analytics` (Finance)  
- 📚 [MongoDB Official Sample Data Documentation](https://www.mongodb.com/docs/atlas/sample-data/)

---

## 📝 Project Structure

```
.
├── app.py                # Streamlit UI
├── agent.py              # Core agent logic (RAG, LLM, fallback)
├── db.py                 # MongoDB connection and helpers
├── memory.py             # Conversation memory
├── requirements.txt      # Python dependencies
└── README.md             # Project overview
```

---

## 🧠 Design & Implementation Notes

- **No hardcoded prompts**: Everything is generated dynamically by LLM + RAG logic.
- **Handles all query types**: Filters, joins, aggregations, nested fields, comparisons, and more.
- **Type-robust**: Deals with data type mismatches and nested fields intelligently.
- **Extensible**: Easily add more collections, context memory, or dashboard features.
- **Error Aware**: Detects ambiguous queries and provides helpful suggestions.

---

## 🌱 Future Enhancements (Bonus Ideas)

- **Vector Similarity Search**: Integrate MongoDB Atlas Search or Pinecone for semantic queries.
- **Streamlit Dashboard**: Add charts and visualizations for trends and summaries.
- **Voice Interface**: Integrate with Web Speech API or Python speech libraries.
- **Docker Support**: Add Dockerfile for easy deployment.
- **Advanced Reasoning**: Use agent frameworks like LangChain or Haystack for chained, multi-step logic.

---


## 📜 License

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for more information.

---

## 🤝 Acknowledgements

- [MongoDB Atlas Sample Datasets](https://www.mongodb.com/docs/atlas/sample-data/)
- [Ollama](https://ollama.com) — Local LLaMA 3 inference engine
- [Streamlit](https://streamlit.io) — For the UI
- All open-source contributors and tools that made this possible

---

## ❓ Questions?

Open an issue or contact me at:  
📧 **reddykasivisweswar@gmail.com**  

