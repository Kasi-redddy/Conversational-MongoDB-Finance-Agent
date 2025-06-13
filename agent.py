import requests
import re
from db import get_collection_names, get_field_names, find_in_collection, aggregate_in_collection

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"

def nl_to_db_query(user_input, memory):
    collections = get_collection_names()
    schema_info = {c: get_field_names(c) for c in collections}
    context = "\n".join([f"User: {h['user']}\nAgent: {h['agent']}" for h in memory.get_context()])
    prompt = f"""
You are an expert assistant for a finance MongoDB database called 'sample_analytics'.
Collections: {collections}
Schema: {schema_info}
Given the user question and recent conversation, generate a valid MongoDB query for either find() or aggregate() and specify:
Type: <find or aggregate>
Collection: <collection>
Query: <query as a valid MongoDB find() filter (dict) or aggregation pipeline (list)>
Projection: <projection dict or null>
Return only the above, no extra text.

Context:
{context}

User question: {user_input}
"""
    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}
        )
        answer = response.json()["response"].strip()
        type_match = re.search(r"Type:\s*(find|aggregate)", answer, re.I)
        coll_match = re.search(r"Collection:\s*(\w+)", answer)
        query_match = re.search(r"Query:\s*(\[.*\]|\{.*\})", answer, re.DOTALL)
        proj_match = re.search(r"Projection:\s*(\{.*\}|null)", answer, re.DOTALL)
        if type_match and coll_match and query_match:
            query_type = type_match.group(1).lower()
            collection = coll_match.group(1)
            query_str = query_match.group(1)
            query = eval(query_str)
            projection = None
            if proj_match and proj_match.group(1) != "null":
                projection = eval(proj_match.group(1))
            return query_type, collection, query, projection, answer
        else:
            return None, None, None, None, answer
    except Exception as e:
        return None, None, None, None, str(e)

def get_answer(user_input, memory):
    query_type, collection, query, projection, llm_raw = nl_to_db_query(user_input, memory)
    # If LLM output is valid, execute as usual
    if collection and query:
        try:
            if isinstance(projection, set):
                projection = {field: 1 for field in projection}
            if query_type == "find":
                results = find_in_collection(collection, query, projection)
            elif query_type == "aggregate":
                results = aggregate_in_collection(collection, query)
            else:
                return "Sorry, I couldn't determine the type of query to execute."
            if results and not isinstance(results[0], str):
                return format_documents(results, f"Results from '{collection}'")
        except Exception as e:
            return f"Error querying database: {e}\nLLM output for debugging:\n{llm_raw}"

    # Fallback: If user input contains an email, search customers by email (case-insensitive)
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', user_input)
    if email_match:
        email = email_match.group(0)
        results = find_in_collection(
            "customers",
            {"email": {"$regex": f"^{email}$", "$options": "i"}}
        )
        if results and not isinstance(results[0], str):
            return format_documents(results, f"Customer details for {email}")
        else:
            return f"No customer found with email {email}."

    # Fallback: Try matching collection names
    user_input_lc = user_input.lower()
    for coll in get_collection_names():
        if coll in user_input_lc:
            results = find_in_collection(coll, {})
            return format_documents(results, f"Results from '{coll}' (fallback)") + \
                   f"\n\nLLM output for debugging:\n{llm_raw}"

    # Fallback: Try extracting a name and searching in customers
    name_match = re.search(r"([A-Z][a-z]+ [A-Z][a-z]+)", user_input)
    if name_match:
        customer_name = name_match.group(1)
        customer = find_in_collection(
            "customers",
            {"name": {"$regex": f"^{customer_name}$", "$options": "i"}},
            limit=1
        )
        if customer:
            return format_documents(customer, f"Customer data for '{customer_name}' (fallback)") + \
                   f"\n\nLLM output for debugging:\n{llm_raw}"

    # Fallback: Try extracting account_id and searching in accounts
    id_match = re.search(r'account_id\s*([0-9]+)', user_input)
    if id_match:
        account_id = id_match.group(1)
        results = find_in_collection(
            "accounts",
            {"$or": [{"account_id": account_id}, {"account_id": int(account_id)}]}
        )
        if results and not isinstance(results[0], str):
            # Try to find the customer who owns this account
            customer = find_in_collection(
                "customers",
                {"accounts": {"$in": [account_id, int(account_id)]}}
            )
            owner_info = ""
            if customer and not isinstance(customer[0], str):
                owner_info = f"\n- **Owned by:** {customer[0].get('name', 'Unknown')}"
            return format_documents(results, f"Account details for ID {account_id}") + owner_info
        else:
            return f"No account found with account_id {account_id}. Please check the ID or try another."

    # Otherwise, show error and LLM output
    return (
        "Sorry, I couldn't understand your question or the AI generated an invalid query.\n"
        f"LLM output for debugging:\n{llm_raw}"
    )

def format_documents(docs, title):
    if not docs or isinstance(docs[0], str):
        return f"{title}: No data found or error."
    output = f"### {title}\n"
    for doc in docs:
        doc_str = []
        for k, v in doc.items():
            if k not in ['_id']:
                doc_str.append(f"- **{k.capitalize()}**: {v}")
        output += "\n".join(doc_str) + "\n---\n"
    return output


