import re 
import json 
with open("agile.txt", "r", encoding="utf-8") as f:
    text = f.read()

def clean(text):
    if not isinstance(text, str):
        return ""
    return " ".join(text.split())

def strip_metadata(text):
    # # Remove Capgemini and broken OCR variants (capg...ini)
    


    text = re.sub(r"cap\w{0,5}ini\w*", "", text, flags=re.IGNORECASE)

    # Remove Page X/XX (with OCR noise allowed)
    text = re.sub(r"page\s*\d+\s*[/\-]\s*\d+", "", text, flags=re.IGNORECASE)

    # Remove standalone PAGE BREAK
    text = re.sub(r"-*\s*page\s*break\s*-*", "", text, flags=re.IGNORECASE)

    text = text.replace("\u00ae" , " ")
    # # Remove training metadata like Type:, Skill:, Score:, etc.
    # text = re.sub(r"Type:.*?sec", "", text, flags=re.DOTALL | re.IGNORECASE)
    # text = re.sub(r"Score:.*?times", "", text, flags=re.DOTALL | re.IGNORECASE)
    # text = re.sub(r"Skill:.*?Status:", "", text, flags=re.DOTALL | re.IGNORECASE)

    # # Final whitespace cleanup
    return clean(text)

def parseq(ocr):
    results = []

    # Split into blocks by "Question #<num>"
    blocks = re.split(r"Question\s*#\d+", ocr, flags=re.IGNORECASE)

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        # Split question and answer
        qa = re.split(r"Answer:\s*", block, maxsplit=1, flags=re.IGNORECASE)

        if len(qa) < 2:
            continue  # No answer → skip block

        raw_question = qa[0].strip()
        raw_answer = qa[1].strip()

        ques = clean(raw_question)

        ans = clean(raw_answer)
        
        ans = ans.split("Question")[0]
        ans = ans

        # Detect correctness
        is_correct = bool(re.search(r"Correct", block, flags=re.IGNORECASE))

        results.append({
            "question": ques,
            "answer": ans,
            "is_correct": is_correct
        })

    return results

ocr_text = text


data = parseq(ocr_text)
print(json.dumps(data, indent=4))
