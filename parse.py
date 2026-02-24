import re 
import json 
import os
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
        parts1 = ques.split("sec")
        ques = parts1[-1].strip()

        ans = clean(raw_answer)
        
        ans = ans.split("Question")[0]
        ans = ans.split("Cap")[0]
        ans = ans.split("Disclaimer")[0]
        parts = ans.split("sec")
        ans = parts[-1].strip()
        

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
# print(json.dumps(data, indent=4))


ls  = ['agile.txt', 'cloud.txt', 'leadersjip.txt']

for i in ls : 
    with open(i , "r" , encoding="utf-8") as f : 
        content = f.read()
        parsed_Data = parseq(content)
    jsonflname = os.path.splitext(i)[0] + ".json"
    with open(jsonflname , "w" , encoding="utf-8") as out : 
        json.dump(parsed_Data , out , indent = 4 )

print("complete")