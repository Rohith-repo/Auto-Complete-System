from flask import Flask, request, jsonify, render_template
import os
from collections import defaultdict

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.frequency = 0  # Track word usage frequency

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.frequency += 1  # Increase word frequency

    def search_prefix(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def get_top_suggestions(self, prefix, top_n=10):
        node = self.search_prefix(prefix)
        if not node:
            return []

        suggestions = []
        self._dfs(node, prefix, suggestions)
        suggestions.sort(key=lambda x: -x[1])  # Sort by frequency (descending)
        return [word for word, _ in suggestions[:top_n]]

    def _dfs(self, node, prefix, suggestions):
        if node.is_end_of_word:
            suggestions.append((prefix, node.frequency))
        for char, child in node.children.items():
            self._dfs(child, prefix + char, suggestions)

app = Flask(__name__)
trie = Trie()
WORDS_FILE = "words_alpha.txt"
word_freq = defaultdict(int)  # Dictionary to track word frequencies

# Load words from file
def load_words():
    if os.path.exists(WORDS_FILE):
        with open(WORDS_FILE, "r") as f:
            for line in f:
                word, freq = line.strip().split(",") if "," in line else (line.strip(), 1)
                word_freq[word] = int(freq)
                for _ in range(int(freq)):  # Insert word multiple times based on frequency
                    trie.insert(word)

def save_word(word):
    word_freq[word] += 1
    with open(WORDS_FILE, "w") as f:
        for word, freq in word_freq.items():
            f.write(f"{word},{freq}\n")

# Load words on startup
load_words()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('query', '').lower().strip()
    if not query:
        return jsonify([])

    suggestions = trie.get_top_suggestions(query)
    if not suggestions:
        save_word(query)  # Save new words
    return jsonify(suggestions)

if __name__ == '__main__':
    app.run(debug=True)
