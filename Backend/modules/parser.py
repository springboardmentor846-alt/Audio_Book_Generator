import json
import re

def parse_study_output(raw):
    try:
        # ---------------- EXTRACT BLOCKS ---------------- #

        content_match = re.search(r"===CONTENT===([\s\S]*?)===QA===", raw)
        qa_match = re.search(r"===QA===([\s\S]*?)===MINDMAP===", raw)
        mindmap_match = re.search(r"===MINDMAP===([\s\S]*)", raw)

        content = content_match.group(1).strip() if content_match else ""
        qa_block = qa_match.group(1).strip() if qa_match else ""
        mindmap_block = mindmap_match.group(1).strip() if mindmap_match else "{}"

        # ---------------- PARSE QA ---------------- #

        qa = []
        lines = [line.strip() for line in qa_block.split("\n") if line.strip()]

        i = 0
        while i < len(lines):
            if lines[i].startswith("Q"):
                question = re.sub(r"Q\d*[:.]", "", lines[i]).strip()

                if i + 1 < len(lines) and lines[i + 1].startswith("A"):
                    answer = re.sub(r"A\d*[:.]", "", lines[i + 1]).strip()
                    qa.append({
                        "question": question,
                        "answer": answer
                    })
                    i += 2
                else:
                    i += 1
            else:
                i += 1

        # ---------------- PARSE MINDMAP ---------------- #

        try:
            mindmap = json.loads(mindmap_block)
        except:
            mindmap = {"name": "Error", "children": []}

        # ---------------- FINAL OUTPUT ---------------- #

        return {
            "notes": content,
            "qa": qa,
            "mindmap": mindmap
        }

    except Exception as e:
        print("Parsing error:", e)
        return {
            "notes": raw,
            "qa": [],
            "mindmap": {}
        }