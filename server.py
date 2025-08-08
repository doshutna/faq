from flask import Flask, request, jsonify
import json
import subprocess
import re

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

FAQ_JSON = "faq.json"
INDEX_HTML = "index.html"

def update_index_html():
    # 1. faq.json 읽기
    with open(FAQ_JSON, encoding='utf-8') as f:
        faqs = json.load(f)
    # 2. index.html 읽기
    with open(INDEX_HTML, encoding='utf-8') as f:
        html = f.read()
    # 3. faqs 배열 부분 치환
    faqs_str = json.dumps(faqs, ensure_ascii=False, indent=2)
    pattern = r'const faqs = \[.*?\];'
    new_faqs_js = f'const faqs = {faqs_str};'
    html = re.sub(pattern, new_faqs_js, html, flags=re.DOTALL)
    # 4. 저장
    with open(INDEX_HTML, 'w', encoding='utf-8') as f:
        f.write(html)

@app.route('/add_faq', methods=['POST'])
def add_faq():
    data = request.get_json()
    q = data.get('q', '').strip()
    a = data.get('a', [])
    c = data.get('c', '').strip()
    if not q or not a or not c:
        return jsonify({"error": "질문/답변/카테고리 모두 필요"}), 400
    # 1. 기존 FAQ 불러오기
    with open(FAQ_JSON, encoding='utf-8') as f:
        faqs = json.load(f)
    # 2. 추가
    faqs.append({"q": q, "a": a, "c": c})
    # 3. 저장
    with open(FAQ_JSON, 'w', encoding='utf-8') as f:
        json.dump(faqs, f, ensure_ascii=False, indent=2)
    # 4. index.html 동기화
    update_index_html()
    # 5. git 커밋/푸시 (faq.bat 실행)
    subprocess.call(["faq.bat"])
    return jsonify({"result": "ok"})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
