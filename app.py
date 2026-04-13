from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Import RAG modules
from rag_answer import rag_answer
from index import list_chunks

app = Flask(__name__)
CORS(app)

@app.route('/api/query', methods=['POST'])
def query_api():
    try:
        data = request.json
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({'error': 'Question cannot be empty'}), 400
        
        # Call RAG pipeline
        result = rag_answer(question)
        
        return jsonify({
            'question': question,
            'answer': result['answer'],
            'sources': result['sources'],
            'retrieval_mode': result.get('retrieval_mode', 'hybrid'),
            'chunks_found': result.get('chunks_found', 0),
            'top_score': result.get('top_score', 0)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def stats_api():
    try:
        chunks = list_chunks()
        return jsonify({
            'total_chunks': len(chunks) if chunks else 0,
            'total_documents': len(set([c['metadata'].get('source', '') for c in chunks if chunks])) if chunks else 0
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5000)
