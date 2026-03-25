🕉️ Pariprashna AI – Enquire Within

Smart Contract Deployed ✅
Contract Address: 0x95d12c98195c126d18a54b3a0de1c62b0c23845e

🚀 Overview

Pariprashna AI – Enquire Within is an AI-powered chatbot inspired by the teachings of the Bhagavad Gita, designed to help users navigate real-life challenges through timeless wisdom.

It combines:

🧠 AI (LLM-based understanding)
🌐 Multilingual support
📘 Sanskrit learning mode
🔗 Blockchain logging (EVM)

Built as a hackathon-ready prototype, the system focuses on simplicity, usability, and meaningful interaction.

🎯 Features
🧠 Context-Aware AI Guidance
Understands user emotions (stress, confusion, purpose, etc.)
Provides relevant Bhagavad Gita shlokas
Gives practical advice, not just philosophy
🌐 Multilingual Support

Supports 3 languages:

English 🇬🇧
Hindi 🇮🇳
Kannada 🟡

Flow:

User Input → Translate → AI Processing → Translate Back → Output
📘 Learn Mode (Unique Feature)
Toggle ON/OFF
When ON:
Provides word-by-word Sanskrit breakdown
When OFF:
Keeps response concise
🔗 Blockchain Logging (EVM Compatible)

Each response is hashed:

keccak(user_input + response)
Logged on blockchain via smart contract
Returns transaction hash (tx_hash)
💬 Chat Interface
Clean, modern UI
Card-based response layout:
🕉 Shloka
📖 Meaning
📚 Word Meaning (Learn Mode)
💡 Advice
🧱 Tech Stack
Backend
FastAPI
OpenAI / Gemini (LLM)
deep-translator
web3.py
Frontend
React
Tailwind CSS
Blockchain
EVM-compatible chain (Shardeum / testnet)
📦 API Endpoints
🔹 POST /chat
Request:
{
  "message": "I feel anxious about my future",
  "language": "en",
  "learn_mode": true
}
Response:
{
  "shloka": "...",
  "meaning": "...",
  "word_meaning": "...",
  "advice": "...",
  "tx_hash": "0x..."
}
🔹 POST /blockchain/log-chat
Request:
{
  "hash": "string"
}
Response:
{
  "tx_hash": "0x..."
}
⚙️ Setup Instructions
1️⃣ Clone Repository
git clone <your-repo-url>
cd pariprashna-ai
2️⃣ Backend Setup
cd backend

python -m venv venv
venv\Scripts\activate   # Windows

pip install -r requirements.txt

Create .env file:

OPENAI_API_KEY=your_key
BLOCKCHAIN_RPC_URL=your_rpc
PRIVATE_KEY=your_private_key
CONTRACT_ADDRESS=0x95d12c98195c126d18a54b3a0de1c62b0c23845e
CHAIN_ID=your_chain_id

Run backend:

uvicorn main:app --reload --port 8081
3️⃣ Frontend Setup
cd frontend

npm install
npm run dev

Open:

http://localhost:5173
🎨 UI Design

Light theme with warm colors:

Background: #FFF7ED
Primary: #F97316
Accent: #FDBA74
Text: #1F2937
🧪 Demo Flow (Recommended)

Ask emotional question:

“I feel anxious about my future”

Show AI response
Enable Learn Mode
Ask again → show Sanskrit breakdown
Switch language (Hindi/Kannada)
Show blockchain tx_hash
⚠️ Notes
This is a prototype, not production-ready
No vector DB / embeddings used
Focus is on simplicity + demo impact
🌟 Future Improvements
Add semantic search for shlokas
Voice input/output
User journaling + history
Better blockchain indexing
🙏 Inspiration

Inspired by the timeless wisdom of the Bhagavad Gita and the concept of Pariprashna — deep, sincere inquiry.

👨‍💻 Author

Built for hackathon by a developer exploring:

AI
Spirituality
Real-world impact
