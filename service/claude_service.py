import anthropic
import config

client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
MODEL = "claude-opus-4-6"


def summarize(text: str) -> dict:
    response = client.messages.create(
        model=MODEL,
        max_tokens=1000,
        system="You are a document analysis assistant. Summarize the following document clearly and concisely. After the summary, on a new line write 'TOPICS:' followed by 5 comma-separated key topics from the document.",
        messages=[
            {"role": "user", "content": f"Document:\n\n{text}"}
        ]
    )

    full_response = response.content[0].text

    if "TOPICS:" in full_response:
        parts = full_response.split("TOPICS:")
        summary_text = parts[0].strip()
        topics = [t.strip() for t in parts[1].split(",")]
    else:
        summary_text = full_response.strip()
        topics = []

    return {
        "summary_text": summary_text,
        "key_topics": topics,
        "model_used": MODEL
    }


def compare(text_a: str, text_b: str) -> str:
    response = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        system="You are a document comparison assistant. Compare the two documents provided and identify key similarities, key differences, what is in document A but not B, what is in document B but not A, and any recommendations.",
        messages=[
            {"role": "user", "content": f"Document A:\n\n{text_a}\n\nDocument B:\n\n{text_b}"}
        ]
    )
    return response.content[0].text


def extract(text: str) -> dict:
    response = client.messages.create(
        model=MODEL,
        max_tokens=1000,
        system="You are a data extraction assistant. Extract structured data from the document. Return ONLY a JSON object with these keys: dates (list of dates found), parties (list of people or company names), amounts (list of monetary amounts). No extra text.",
        messages=[
            {"role": "user", "content": f"Document:\n\n{text}"}
        ]
    )

    import json
    try:
        result = json.loads(response.content[0].text)
    except:
        result = {"dates": [], "parties": [], "amounts": []}

    return result


def chat_stream(question: str, document_text: str, history: list):
    messages = []

    for item in history:
        messages.append({
            "role": item["role"].lower(),
            "content": item["content"]
        })

    messages.append({"role": "user", "content": question})

    with client.messages.stream(
        model=MODEL,
        max_tokens=2000,
        system=f"You are a document assistant. Answer questions based only on the document provided. If the answer is not in the document, say so.\n\nDocument:\n\n{document_text}",
        messages=messages
    ) as stream:
        for text in stream.text_stream:
            yield text