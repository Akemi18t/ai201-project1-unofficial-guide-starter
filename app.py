import gradio as gr
from ingest import ingest_all
from retriever import embed_and_store, retrieve, _collection
from generator import generate_response

# Run ingestion on startup
if _collection.count() == 0:
    print("Ingesting documents...")
    chunks = ingest_all()
    embed_and_store(chunks)
    print("Ingestion complete!")
else:
    print(f"Collection already has {_collection.count()} chunks, skipping ingestion.")


def handle_query(question):
    if not question.strip():
        return "Please enter a question.", ""
    
    chunks = retrieve(question)
    answer = generate_response(question, chunks)
    sources = "\n".join(set(f"• {c['source']}" for c in chunks))
    return answer, sources


with gr.Blocks(title="UDC Unofficial Housing Guide") as demo:
    gr.Markdown("# UDC Unofficial Off-Campus Housing Guide")
    gr.Markdown("Ask anything about off-campus housing near UDC — based on real student experiences.")
    
    inp = gr.Textbox(label="Your question", placeholder="e.g. What are apartments like near Van Ness?")
    btn = gr.Button("Ask")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Sources", lines=4)
    
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

demo.launch()