from flask import Flask, request, jsonify, render_template, request as flask_request
import google.generativeai as genai
import ollama
from openai import OpenAI
import os
from config import GEMINI_API_KEY, OLLAMA_MODEL, OPENAI_API_KEY, ANTHROPIC_API_KEY
from utils import read_code, write_code


app = Flask(__name__)
print("key",OPENAI_API_KEY)
def get_llm_response(code, instruction, llm_type):
    prompt = f"""You are a code fixing and generation expert. 

Current code:
```
{code}
```

Task: {instruction}

Respond ONLY with:
1. Brief explanation of changes.
2. Fixed/improved code in ```python ... ``` block.

Do not add extra text."""

    if llm_type == 'gemini' and GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        return response.text.strip()

    elif llm_type == 'ollama':
        response = ollama.chat(model=OLLAMA_MODEL, messages=[{'role': 'user', 'content': prompt}])
        return response['message']['content'].strip()

    elif llm_type == 'openai' and OPENAI_API_KEY:
        print("yessss")
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[{'role': 'user', 'content': prompt}]
        )
        return response.choices[0].message.content.strip()

    elif llm_type == 'claude' and ANTHROPIC_API_KEY:
        import anthropic
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text.strip()

    else:
        return 'Error: LLM not configured. Check .env and llm param.'

@app.route('/chat', methods=['POST'])
def chat():
    print("enter here")
    code_source = None
    instruction = flask_request.form.get('instruction', '')
    llm_type = flask_request.form.get('llm', 'openai').lower()
    print(instruction,llm_type)
    print(flask_request.form.get('code', ''))
    file = flask_request.files.get('file')
    if file:
        code_source = file.read().decode('utf-8')
    else:
        code_source = flask_request.form.get('code', '')
    if not code_source:
        code_source = ""
    if not instruction:
        return jsonify({'error': 'Missing code or instruction'}), 400

    response = get_llm_response(code_source, instruction, llm_type)

    # Extract fixed code (assume after first ``` block)
    if '```python' in response:
        fixed_code = response.split('```python')[1].split('```')[0].strip()
    else:
        fixed_code = response

    write_status = write_code(code_source if isinstance(code_source, str) and os.path.exists(code_source) else None, fixed_code)

    return jsonify({
        'response': response,
        'fixed_code': fixed_code,
        'write_status': write_status
    })

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

