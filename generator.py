from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
LLM_MODEL = "llama-3.3-70b-versatile"


def generate_response(query, retrieved_chunks):
    if not retrieved_chunks:
        return "I don't have enough information in my documents to answer that question."

    context_blocks = []
    for chunk in retrieved_chunks:
        context_blocks.append(f"[Source: {chunk['source']}]\n{chunk['text']}")
    context = "\n\n".join(context_blocks)

    system_prompt = (
        "You are an Unofficial Guide assistant for UDC students looking for off-campus housing. "
        "Answer the user's question using ONLY the document excerpts provided below. "
        "Do not draw on outside knowledge. "
        "Always mention which source document the answer comes from. "
        "If the answer is not in the provided documents, say clearly: "
        "'I don't have enough information in my documents to answer that.'"
    )

    user_message = f"Document excerpts:\n\n{context}\n\nQuestion: {query}"

    response = _client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        max_tokens=1000
    )

    return response.choices[0].message.content