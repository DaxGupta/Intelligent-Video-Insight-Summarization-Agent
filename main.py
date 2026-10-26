import time
from dotenv import load_dotenv
from utils.audio_processor import process_audio as process_input
from core.transcriber import transcribe_all
from core.extractor import extract_action_items, extract_key_decisions, extract_questions
from core.summarizer import summarize, generate_title
from core.rag_engine import build_rag_chain, ask_question

load_dotenv()

def run_pipeline(source:str, language:str="english")->dict:
    print("starting AI Video Assistant")

    chunks = process_input(source)

    transcript = transcribe_all(chunks)
    print(f"raw transcription (first 300 characters): {transcript[:300]}")

    print("Analyzing transcript and generating deliverables...")
    
    # Sequential API calls with delays to prevent 429 RESOURCE_EXHAUSTED errors
    print("Generating title...")
    title = generate_title(transcript)
    time.sleep(10)
    
    print("Generating summary...")
    summary = summarize(transcript)
    time.sleep(10)
    
    print("Extracting action items...")
    action_items = extract_action_items(transcript)
    time.sleep(10)
    
    print("Extracting key decisions...")
    decisions = extract_key_decisions(transcript)
    time.sleep(10)
    
    print("Extracting questions...")
    questions = extract_questions(transcript)

    analysis = {
        "title": title,
        "summary": summary,
        "action_items": action_items,
        "decisions": decisions,
        "questions": questions
    }

    print("Building RAG chain...")
    rag_chain = build_rag_chain(transcript)

    return {
        "title": analysis.get("title", "Untitled Meeting"),
        "transcript": transcript,
        "summary": analysis.get("summary", "No summary generated."),
        "action_items": analysis.get("action_items", "No action items found."),
        "decisions": analysis.get("decisions", "No key decisions found."),
        "questions": analysis.get("questions", "No questions found."),
        "rag_chain": rag_chain
    }

if __name__ == "__main__":
    source = input("Enter Youtube URL or local file path: ").strip()
    language = input("Enter language (default: english): ").strip() or "english"
    result = run_pipeline(source, language)

    print("\n" + "="*60+"\n")
    print(f"📌 Title: {result['title']}\n")
    print(f"🗒️ Summary: {result['summary']}\n")
    print(f"✅ Action Items: {result['action_items']}\n")
    print(f"🔑 Key Decisions: {result['decisions']}\n")
    print(f"❓ Open Questions: {result['questions']}\n")
    print("="*60+"\n")

    print("\n 💬 Chat with your meeting (type 'exit' to quit):\n")
    rag_chain= result['rag_chain']

    while True:
        question = input("You: ").strip()
        if question.lower() in ["exit", "quit", "q"]:
            print("Exiting chat. 👋 Goodbye!")
            break
        if not question:
            continue
        answer = ask_question(rag_chain, question)
        print(f"\n 🤖 Assistant: {answer} \n")