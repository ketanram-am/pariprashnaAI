# 🕉️ Pariprashna AI — Enquire Within

> *Timeless wisdom for modern challenges, powered by AI and the Bhagavad Gita.*

[![Live Demo](https://img.shields.io/badge/Demo-Live%20on%20Vercel-brightgreen)](https://pariprashna-ai-ezoi-4hegl07lf-ketanram-ams-projects.vercel.app/)
[![Smart Contract](https://img.shields.io/badge/Contract-0x95d1...845e-blue)](https://pariprashna-ai-ezoi-4hegl07lf-ketanram-ams-projects.vercel.app/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## Overview

**Pariprashna AI** is an AI-powered chatbot that guides users through real-life challenges using the wisdom of the Bhagavad Gita. Named after the Sanskrit concept of *sincere, deep inquiry*, it responds to emotional and existential questions with relevant shlokas, practical advice, and Sanskrit learning — all logged immutably on the blockchain.

---

## Features

### 🧠 Context-Aware AI Guidance
- Understands user emotions — stress, confusion, purpose, grief, and more
- Surfaces the most relevant Bhagavad Gita shloka for each situation
- Delivers practical, actionable advice alongside philosophical insight

### 🌐 Multilingual Support
Supports four languages with automatic translation:

| Language | Code |
|----------|------|
| English  | `en` |
| Hindi    | `hi` |
| Kannada  | `kn` |
| Telugu   | `te` |

Flow: `User Input → Translate → AI Processing → Translate Back → Output`

### 📘 Learn Mode
Toggle Sanskrit learning on or off:
- **ON** — word-by-word Sanskrit breakdown with meanings
- **OFF** — concise shloka and advice only

### 🔗 Blockchain Logging (EVM)
Every response is cryptographically logged:
1. Hash computed: `keccak256(user_input + response)`
2. Logged via smart contract on an EVM-compatible chain
3. Transaction hash (`tx_hash`) returned in the response

**Contract Address:** `0x95d12c98195c126d18a54b3a0de1c62b0c23845e`

### 💬 Chat Interface
Clean, card-based UI for each response:
- 🕉 Shloka
- 📖 Meaning
- 📚 Word Meaning *(Learn Mode only)*
- 💡 Advice

---

## Tech Stack

| Layer      | Technology                        |
|------------|-----------------------------------|
| Frontend   | React, Tailwind CSS               |
| Backend    | FastAPI (Python)                  |
| AI/LLM     | OpenAI / Gemini                   |
| Translation| deep-translator                   |
| Blockchain | web3.py, EVM (Shardeum / testnet) |

---

## API Reference

### `POST /chat`

**Request:**
```json
{
  "message": "I feel anxious about my future",
  "language": "en",
  "learn_mode": true
}
```

**Response:**
```json
{
  "shloka": "...",
  "meaning": "...",
  "word_meaning": "...",
  "advice": "...",
  "tx_hash": "0x..."
}
```

---

### `POST /blockchain/log-chat`

**Request:**
```json
{
  "hash": "string"
}
```

**Response:**
```json
{
  "tx_hash": "0x..."
}
```

---

## Getting Started

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd pariprashna-ai
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_key
BLOCKCHAIN_RPC_URL=your_rpc_url
PRIVATE_KEY=your_private_key
CONTRACT_ADDRESS=0x95d12c98195c126d18a54b3a0de1c62b0c23845e
CHAIN_ID=your_chain_id
```

Start the server:

```bash
uvicorn main:app --reload --port 8081
```

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## UI Design

| Token       | Value     |
|-------------|-----------|
| Background  | `#FFF7ED` |
| Primary     | `#F97316` |
| Accent      | `#FDBA74` |
| Text        | `#1F2937` |

Warm, minimal, and distraction-free — designed to feel grounding.

---

## Recommended Demo Flow

1. Ask an emotional question: *"I feel anxious about my future"*
2. Review the AI response (shloka + advice)
3. Enable **Learn Mode** and ask again → see Sanskrit word breakdown
4. Switch language to Hindi or Kannada
5. Note the `tx_hash` in the response — the interaction is on-chain

---

## Roadmap

- [ ] Semantic search over shloka embeddings (vector DB)
- [ ] Voice input and text-to-speech output
- [ ] User journaling and conversation history
- [ ] On-chain indexing and query support
- [ ] Mobile app (React Native)

---

## Notes

This is a hackathon prototype focused on simplicity and demo impact. It does not use vector embeddings or production-grade infrastructure yet.

---

## Inspiration

*"Pariprashna"* — deep, sincere inquiry — is the act of approaching a teacher with genuine questions. This project brings that spirit into the age of AI, making the Gita's wisdom accessible to anyone, anywhere, in their own language.

---

## Author

Built for a hackathon by a developer at the intersection of **AI**, **spirituality**, and **real-world impact**.

*Contributions and feedback welcome.*
