# 🕉️ Pariprashna AI – Enquire Within

An AI-powered, multilingual chatbot that provides **authentic Bhagavad Gita-based guidance** for real-life problems, with verified shloka references and blockchain-backed integrity.

---

## 🚀 Overview

Pariprashna AI is a domain-specific chatbot designed to bridge **modern human challenges** with **timeless wisdom from the Bhagavad Gita**.

Unlike generic AI chatbots, this system:

* Grounds every response in **real Bhagavad Gita verses**
* Displays **chapter and verse references**
* Provides **practical, actionable advice**
* Supports **multilingual interaction**
* Ensures **response integrity using blockchain hashing**

---

## 🎯 Key Features

### 🧠 Intelligent Problem Understanding

* Uses AI (OpenAI/Gemini) to analyze user input
* Classifies problems (stress, fear, confusion, discipline, existential)

### 📖 Authentic Gita-Based Responses

* Sanskrit **shloka**
* 📍 Chapter & Verse reference
* 📖 Simple meaning
* 💡 Practical life advice

### 🌍 Multilingual Support

* English (EN)
* हिंदी (HI)
* ಕನ್ನಡ (KN)

> Input can be in any language, output is delivered in selected language.

---

### 🎓 Learn Mode (Sanskrit Breakdown)

* Toggle ON to view **word-by-word Sanskrit meaning**
* Helps users deeply understand each verse

---

### ⛓ Blockchain Logging

* Each response is hashed using SHA-256
* Stored on EVM-compatible blockchain
* Ensures **tamper-proof responses**

Output includes:

```
Hash: ab12cd34ef
Tx: logged / not logged
```

---

## 🏗️ Tech Stack

### Backend

* FastAPI
* OpenAI / Gemini API
* deep-translator
* web3.py

### Frontend

* React
* Tailwind CSS

---

## 🧩 Project Structure

```
pariprashna-ai/
│
├── backend/
│   ├── main.py
│   ├── gita_data.py
│   ├── blockchain.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/Chat.jsx
│   │   └── styles.css
│   └── package.json
```

---

## ⚙️ How It Works

1. User inputs query (EN / HI / KN)
2. Input translated → English
3. AI analyzes and classifies intent
4. System retrieves relevant Bhagavad Gita verse:

   * Primary: local dataset
   * Fallback: AI (strict validation)
5. Generates structured response:

   * Shloka
   * Reference
   * Meaning
   * Advice
6. Response translated → selected language
7. Hash generated and logged on blockchain

---

## ▶️ Running Locally

### 🔧 Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

---

### 💻 Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 🌍 Language Toggle (UI)

The app includes **3 fixed toggle buttons**:

```
[ English ] [ हिंदी ] [ ಕನ್ನಡ ]
```

* Only one active at a time
* Default: English
* Sanskrit text is never translated

---

## 📦 Sample Response

```
🕉 Shloka:
देहिनोऽस्मिन्यथा देहे कौमारं यौवनं जरा...

📍 Reference:
Bhagavad Gita Chapter 2, Verse 13

📖 Meaning:
Just as the soul passes through childhood, youth, and old age...

💡 Advice:
Do not fear change. Your true identity is beyond the body.

🔗 Source:
Based on Bhagavad Gita Chapter 2, Verse 13

Hash: ab12cd34ef
Tx: logged
```

---

## ⚠️ Constraints

* No database used
* No vector search
* Minimal dependencies
* Designed for **hackathon demo reliability**

---

## 🎯 Vision

> “We do not generate scripture — we interpret it.”

Pariprashna AI aims to make the Bhagavad Gita:

* Accessible
* Understandable
* Practically applicable in daily life

---

## 🙏 Acknowledgment

Inspired by the timeless teachings of the **Bhagavad Gita** and the need to make spiritual wisdom accessible through modern technology.

---

## 📌 Future Improvements

* Voice input & output 🎤
* Daily shloka recommendations 📅
* User emotion analytics 📊
* Expanded verse dataset 📚

---

## 👨‍💻 Author

Built for hackathons with clarity, simplicity, and impact in mind.

---

✨ *Enquire within. The answers are already there.*
