/**
 * Monaco Editor Customizer & Configurations for HFUTXC OJ
 * Supports Python, C/C++, and Java with custom templates, autocomplete suggestions, and themes.
 */

// Default language templates for the editor
export const templates = {
  cpp: `#include <bits/stdc++.h>
using namespace std;

void solve() {
    
}

int main() {
    cin.tie(0) -> sync_with_stdio(0);
    int t;
    cin >> t;
    while (t--) solve();
}`,
  python: `from math import sqrt, gcd, log; import sys; input = lambda: sys.stdin.readline().strip(); re = lambda: map(int, input().split())

def solve():
    pass

t, = re()

for _ in range(t):
    solve()`,
  java: `import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st;
        
        // Write your code here
        
    }
}`,
  c: `#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void solve() {
    // Write your code here
}

int main() {
    int t = 1;
    // scanf("%d", &t);
    while (t--) {
        solve();
    }
    return 0;
}`,
  go: `package main

import (
	"bufio"
	"fmt"
	"os"
)

func solve(in *bufio.Reader, out *bufio.Writer) {
	// Write your code here
}

func main() {
	in := bufio.NewReader(os.Stdin)
	out := bufio.NewWriter(os.Stdout)
	defer out.Flush()

	var t int = 1
	// fmt.Fscan(in, &t)
	for i := 0; i < t; i++ {
		solve(in, out)
	}
}`,
  rust: `use std::io::{self, BufRead};

fn solve() {
    // Write your code here
}

fn main() {
    let stdin = io::stdin();
    let mut iterator = stdin.lock().lines();
    
    let t = 1;
    for _ in 0..t {
        solve();
    }
}`,
  javascript: `const fs = require('fs');

function solve() {
    const input = fs.readFileSync('/dev/stdin', 'utf-8');
    const lines = input.trim().split('\\n');
    // Write your code here
}

solve();`,
  csharp: `using System;
using System.IO;
using System.Collections.Generic;

class Program {
    static void Solve() {
        // Write your code here
    }

    static void Main() {
        int t = 1;
        while (t-- > 0) {
            Solve();
        }
    }
}`,
  kotlin: `import java.io.BufferedReader
import java.io.InputStreamReader
import java.util.StringTokenizer

fun solve() {
    // Write your code here
}

fun main() {
    val reader = BufferedReader(InputStreamReader(System.\`in\`))
    var tokenizer: StringTokenizer? = null

    fun nextToken(): String {
        while (tokenizer == null || !tokenizer!!.hasMoreTokens()) {
            val line = reader.readLine() ?: return ""
            tokenizer = StringTokenizer(line)
        }
        return tokenizer!!.nextToken()
    }

    val t = 1
    for (i in 0 until t) {
        solve()
    }
}`
}

// Custom VS Code Dark+ theme definition
export const registerVscodeDarkTheme = (monaco) => {
  monaco.editor.defineTheme('vscode-dark', {
    base: 'vs-dark',
    inherit: true,
    rules: [
      { token: 'comment', foreground: '6A9955', fontStyle: 'italic' },
      { token: 'keyword', foreground: '569CD6' },
      { token: 'number', foreground: 'B5CEA8' },
      { token: 'string', foreground: 'CE9178' },
      { token: 'type', foreground: '4EC9B0' },
      { token: 'class', foreground: '4EC9B0' },
      { token: 'struct', foreground: '4EC9B0' },
      { token: 'interface', foreground: '4EC9B0' },
      { token: 'function', foreground: 'DCDCAA' },
      { token: 'variable', foreground: '9CDCFE' },
      { token: 'operator', foreground: 'D4D4D4' },
      // Custom green colors for specific tokens
      { token: 'keyword.type', foreground: '4EC9B0' },
      { token: 'type.identifier', foreground: '4EC9B0' }
    ],
    colors: {
      'editor.background': '#1E1E1E',
      'editor.foreground': '#D4D4D4',
      'editorCursor.foreground': '#AEAFAD',
      'editor.lineHighlightBackground': '#2D2D30',
      'editorLineNumber.foreground': '#858585',
      'editorLineNumber.activeForeground': '#C6C6C6',
    }
  })
}

// Registers custom autocompletions for Python, C++, and Java in Monaco
export const registerCustomCompletions = (monaco) => {
  // 1. C++ Suggestions
  monaco.languages.registerCompletionItemProvider('cpp', {
    provideCompletionItems: (model, position) => {
      const word = model.getWordUntilPosition(position);
      const range = {
        startLineNumber: position.lineNumber,
        endLineNumber: position.lineNumber,
        startColumn: word.startColumn,
        endColumn: word.endColumn
      };

      const suggestions = [
        // Standard containers (Classes)
        {
          label: 'vector',
          kind: monaco.languages.CompletionItemKind.Class,
          insertText: 'vector<${1:int}>',
          insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          detail: 'std::vector dynamic array',
          range
        },
        {
          label: 'unordered_map',
          kind: monaco.languages.CompletionItemKind.Class,
          insertText: 'unordered_map<${1:int}, ${2:int}>',
          insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          detail: 'std::unordered_map hash table',
          range
        },
        {
          label: 'map',
          kind: monaco.languages.CompletionItemKind.Class,
          insertText: 'map<${1:int}, ${2:int}>',
          insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          detail: 'std::map red-black tree map',
          range
        },
        {
          label: 'unordered_set',
          kind: monaco.languages.CompletionItemKind.Class,
          insertText: 'unordered_set<${1:int}>',
          insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          detail: 'std::unordered_set hash set',
          range
        },
        {
          label: 'set',
          kind: monaco.languages.CompletionItemKind.Class,
          insertText: 'set<${1:int}>',
          insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          detail: 'std::set red-black tree set',
          range
        },
        {
          label: 'string',
          kind: monaco.languages.CompletionItemKind.Class,
          insertText: 'string',
          detail: 'std::string dynamic character array',
          range
        },
        {
          label: 'pair',
          kind: monaco.languages.CompletionItemKind.Class,
          insertText: 'pair<${1:int}, ${2:int}>',
          insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          detail: 'std::pair tuple wrapper',
          range
        },

        // Fast IO Snippet
        {
          label: 'fastio',
          kind: monaco.languages.CompletionItemKind.Snippet,
          insertText: 'ios::sync_with_stdio(false);\ncin.tie(nullptr);$0',
          insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          detail: 'C++ Fast I/O optimize streams',
          range
        },

        // Algorithmic Snippets (DSU, qpow, gcd)
        {
          label: 'dsu',
          kind: monaco.languages.CompletionItemKind.Snippet,
          insertText: 'struct DSU {\n\tvector<int> parent;\n\tDSU(int n) {\n\t\tparent.resize(n);\n\t\tiota(parent.begin(), parent.end(), 0);\n\t}\n\tint find(int i) {\n\t\tif (parent[i] == i) return i;\n\t\treturn parent[i] = find(parent[i]);\n\t}\n\tvoid unite(int i, int j) {\n\t\tint root_i = find(i);\n\t\tint root_j = find(j);\n\t\tif (root_i != root_j) parent[root_i] = root_j;\n\t}\n};$0',
          insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          detail: 'Disjoint Set Union (并查集) Template',
          range
        },
        {
          label: 'qpow',
          kind: monaco.languages.CompletionItemKind.Snippet,
          insertText: 'long long qpow(long long base, long long exp) {\n\tlong long res = 1;\n\tbase %= ${1:1000000007};\n\twhile (exp > 0) {\n\t\tif (exp % 2 == 1) res = (res * base) % ${1:1000000007};\n\t\tbase = (base * base) % ${1:1000000007};\n\t\texp /= 2;\n\t}\n\treturn res;\n}$0',
          insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          detail: 'Quick Power (快速幂) with Modulo',
          range
        },
        {
          label: 'gcd',
          kind: monaco.languages.CompletionItemKind.Snippet,
          insertText: 'long long gcd(long long a, long long b) {\n\treturn b == 0 ? a : gcd(b, a % b);\n}$0',
          insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          detail: 'GCD (最大公约数) Template',
          range
        },

        // C++ loops
        {
          label: 'fori',
          kind: monaco.languages.CompletionItemKind.Snippet,
          insertText: 'for (int i = 0; i < ${1:n}; ++i) {\n\t$0\n}',
          insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          detail: 'standard index-based for loop',
          range
        },
        {
          label: 'forj',
          kind: monaco.languages.CompletionItemKind.Snippet,
          insertText: 'for (int j = 0; j < ${1:m}; ++j) {\n\t$0\n}',
          insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          detail: 'nested index-based for loop',
          range
        },
        {
          label: 'foreach',
          kind: monaco.languages.CompletionItemKind.Snippet,
          insertText: 'for (const auto& ${1:x} : ${2:container}) {\n\t$0\n}',
          insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          detail: 'range-based for loop',
          range
        }
      ];

      return { suggestions };
    }
  });

  // 2. Python Suggestions
  monaco.languages.registerCompletionItemProvider('python', {
    provideCompletionItems: (model, position) => {
      const word = model.getWordUntilPosition(position);
      const range = {
        startLineNumber: position.lineNumber,
        endLineNumber: position.lineNumber,
        startColumn: word.startColumn,
        endColumn: word.endColumn
      };

      const suggestions = [
        // Standard library shortcuts
        {
          label: 'defaultdict',
          kind: monaco.languages.CompletionItemKind.Class,
          insertText: 'defaultdict(${1:list})',
          insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          detail: 'from collections import defaultdict',
          range
        },
        {
          label: 'Counter',
          kind: monaco.languages.CompletionItemKind.Class,
          insertText: 'Counter(${1:iterable})',
          insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          detail: 'from collections import Counter dict counter',
          range
        },
        {
          label: 'deque',
          kind: monaco.languages.CompletionItemKind.Class,
          insertText: 'deque()',
          detail: 'from collections import deque double-ended queue',
          range
        },
        {
          label: 'sysinput',
          kind: monaco.languages.CompletionItemKind.Snippet,
          insertText: 'input = lambda: sys.stdin.readline().strip()$0',
          insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          detail: 'Python Fast I/O stdin readline',
          range
        },

        // Algorithmic Snippets
        {
          label: 'dsu',
          kind: monaco.languages.CompletionItemKind.Snippet,
          insertText: 'class DSU:\n    def __init__(self, n):\n        self.parent = list(range(n))\n    def find(self, i):\n        if self.parent[i] == i:\n            return i\n        self.parent[i] = self.find(self.parent[i])\n        return self.parent[i]\n    def unite(self, i, j):\n        root_i = self.find(i)\n        root_j = self.find(j)\n        if root_i != root_j:\n            self.parent[root_i] = root_j$0',
          insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          detail: 'Disjoint Set Union (并查集) Template',
          range
        },
        {
          label: 'qpow',
          kind: monaco.languages.CompletionItemKind.Snippet,
          insertText: 'def qpow(base, exp, mod=10**9 + 7):\n    return pow(base, exp, mod)$0',
          insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          detail: 'Quick Power (快速幂) with Modulo',
          range
        },
        {
          label: 'gcd',
          kind: monaco.languages.CompletionItemKind.Snippet,
          insertText: 'def gcd(a, b):\n    while b:\n        a, b = b, a % b\n    return a$0',
          insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          detail: 'GCD (最大公约数) Template',
          range
        },

        // Common snippets
        {
          label: 'fori',
          kind: monaco.languages.CompletionItemKind.Snippet,
          insertText: 'for i in range(${1:n}):\n\t$0',
          insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          detail: 'for i in range loop',
          range
        },
        {
          label: 'def',
          kind: monaco.languages.CompletionItemKind.Snippet,
          insertText: 'def ${1:func_name}(${2:args}):\n\t$0',
          insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          detail: 'define custom function',
          range
        }
      ];

      return { suggestions };
    }
  });

  // 3. Java Suggestions
  monaco.languages.registerCompletionItemProvider('java', {
    provideCompletionItems: (model, position) => {
      const word = model.getWordUntilPosition(position);
      const range = {
        startLineNumber: position.lineNumber,
        endLineNumber: position.lineNumber,
        startColumn: word.startColumn,
        endColumn: word.endColumn
      };

      const suggestions = [
        // Standard Collections & Classes
        {
          label: 'ArrayList',
          kind: monaco.languages.CompletionItemKind.Class,
          insertText: 'ArrayList<${1:Integer}>',
          insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          detail: 'java.util.ArrayList dynamic array list',
          range
        },
        {
          label: 'HashMap',
          kind: monaco.languages.CompletionItemKind.Class,
          insertText: 'HashMap<${1:Integer}, ${2:Integer}>',
          insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          detail: 'java.util.HashMap key-value dictionary table',
          range
        },
        {
          label: 'HashSet',
          kind: monaco.languages.CompletionItemKind.Class,
          insertText: 'HashSet<${1:Integer}>',
          insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          detail: 'java.util.HashSet lookup set',
          range
        },
        {
          label: 'List',
          kind: monaco.languages.CompletionItemKind.Interface,
          insertText: 'List<${1:Integer}>',
          insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          detail: 'java.util.List list interface',
          range
        },
        {
          label: 'Map',
          kind: monaco.languages.CompletionItemKind.Interface,
          insertText: 'Map<${1:Integer}, ${2:Integer}>',
          insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          detail: 'java.util.Map map interface',
          range
        },
        {
          label: 'PriorityQueue',
          kind: monaco.languages.CompletionItemKind.Class,
          insertText: 'PriorityQueue<${1:Integer}>',
          insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          detail: 'java.util.PriorityQueue binary heap priority queue',
          range
        },

        // Algorithmic Snippets
        {
          label: 'dsu',
          kind: monaco.languages.CompletionItemKind.Snippet,
          insertText: 'static class DSU {\n\t    int[] parent;\n\t    DSU(int n) {\n\t        parent = new int[n];\n\t        for (int i = 0; i < n; i++) parent[i] = i;\n\t    }\n\t    int find(int i) {\n\t        if (parent[i] == i) return i;\n\t        return parent[i] = find(parent[i]);\n\t    }\n\t    void unite(int i, int j) {\n\t        int rootI = find(i);\n\t        int rootJ = find(j);\n\t        if (rootI != rootJ) parent[rootI] = rootJ;\n\t    }\n\t}$0',
          insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          detail: 'Disjoint Set Union (并查集) static class',
          range
        },
        {
          label: 'qpow',
          kind: monaco.languages.CompletionItemKind.Snippet,
          insertText: 'static long qpow(long base, long exp) {\n\t    long res = 1;\n\t    base %= 1000000007;\n\t    while (exp > 0) {\n\t        if (exp % 2 == 1) res = (res * base) % 1000000007;\n\t        base = (base * base) % 1000000007;\n\t        exp /= 2;\n\t    }\n\t    return res;\n\t}$0',
          insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          detail: 'Quick Power (快速幂) static method',
          range
        },
        {
          label: 'gcd',
          kind: monaco.languages.CompletionItemKind.Snippet,
          insertText: 'static long gcd(long a, long b) {\n\t    return b == 0 ? a : gcd(b, a % b);\n\t}$0',
          insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          detail: 'GCD (最大公约数) static method',
          range
        },

        // Common standard shortcuts & Snippets
        {
          label: 'sysout',
          kind: monaco.languages.CompletionItemKind.Snippet,
          insertText: 'System.out.println($0);',
          insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          detail: 'System.out.println stdout shortcut',
          range
        },
        {
          label: 'fori',
          kind: monaco.languages.CompletionItemKind.Snippet,
          insertText: 'for (int i = 0; i < ${1:n}; i++) {\n\t$0\n}',
          insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          detail: 'index-based Java loop',
          range
        },
        {
          label: 'main',
          kind: monaco.languages.CompletionItemKind.Snippet,
          insertText: 'public static void main(String[] args) {\n\t$0\n}',
          insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
          detail: 'main method signature',
          range
        }
      ];

      return { suggestions };
    }
  });
}
