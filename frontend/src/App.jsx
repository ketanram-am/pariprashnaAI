import { useEffect, useRef, useState } from "react";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8081";

const SUGGESTIONS = [
  "I feel anxious about my exams.",
  "My mind keeps overthinking every night.",
  "I am dealing with conflict at home.",
  "Work pressure is making me restless.",
];

const LANGUAGE_OPTIONS = [
  { value: "auto", label: "Auto (Detect)" },
  { value: "en", label: "English" },
  { value: "hi", label: "Hindi" },
  { value: "te", label: "Telugu" },
  { value: "kn", label: "Kannada" },
];

function App() {
  const [learnMode, setLearnMode] = useState(false);
  const [targetLanguage, setTargetLanguage] = useState("auto");
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const feedRef = useRef(null);

  useEffect(() => {
    if (feedRef.current) {
      feedRef.current.scrollTop = feedRef.current.scrollHeight;
    }
  }, [messages, isLoading]);

  async function sendMessage(text) {
    const trimmed = text.trim();
    if (!trimmed || isLoading) {
      return;
    }

    const userMessage = {
      id: Date.now(),
      role: "user",
      content: trimmed,
    };

    setError("");
    setMessages((current) => [...current, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: trimmed,
          learn_mode: learnMode,
          target_language: targetLanguage === "auto" ? null : targetLanguage,
        }),
      });

      if (!response.ok) {
        const payload = await response.json().catch(() => ({}));
        throw new Error(payload.detail || "Unable to reach the backend.");
      }

      const payload = await response.json();
      setMessages((current) => [
        ...current,
        {
          id: Date.now() + 1,
          role: "assistant",
          content: payload,
        },
      ]);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsLoading(false);
    }
  }

  function handleSubmit(event) {
    event.preventDefault();
    sendMessage(input);
  }

  function handleKeyDown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage(input);
    }
  }

  return (
    <div className="shell">
      <div className="aurora aurora-one" />
      <div className="aurora aurora-two" />

      <main className="app-card">
        <section className="hero">
          <p className="eyebrow">Pariprashna AI</p>
          <h1>Enquire Within</h1>
          <p className="subtitle">
            A Bhagavad Gita chatbot for reflection, practical guidance, multilingual
            conversations, and word-by-word Sanskrit learning.
          </p>

          <div className="hero-controls">
            <label className={`toggle ${learnMode ? "toggle-on" : ""}`}>
              <input
                type="checkbox"
                checked={learnMode}
                onChange={() => setLearnMode((value) => !value)}
              />
              <span className="toggle-track">
                <span className="toggle-thumb" />
              </span>
              <span className="toggle-copy">
                <strong>Learn Mode</strong>
                <small>{learnMode ? "Word meanings included" : "Compact guidance only"}</small>
              </span>
            </label>

            <label className="language-select">
              <span>Response Language</span>
              <select
                value={targetLanguage}
                onChange={(event) => setTargetLanguage(event.target.value)}
              >
                {LANGUAGE_OPTIONS.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </label>
          </div>

          <div className="suggestions">
            {SUGGESTIONS.map((suggestion) => (
              <button
                key={suggestion}
                type="button"
                className="suggestion-chip"
                onClick={() => sendMessage(suggestion)}
              >
                {suggestion}
              </button>
            ))}
          </div>
        </section>

        <section className="chat-panel">
          <div className="chat-feed" ref={feedRef}>
            {messages.length === 0 ? (
              <div className="empty-state">
                <p className="empty-title">Start with any problem in your own language.</p>
                <p className="empty-copy">
                  The backend translates your message, finds a fitting Gita verse, and
                  sends the response back in your language.
                </p>
              </div>
            ) : null}

            {messages.map((message) =>
              message.role === "user" ? (
                <article key={message.id} className="message-row user-row">
                  <div className="user-bubble">{message.content}</div>
                </article>
              ) : (
                <article key={message.id} className="message-row assistant-row">
                  <div className="assistant-card">
                    <div className="shloka-block">
                      <p className="section-label">Shloka</p>
                      <p className="shloka-text">{message.content.shloka}</p>
                    </div>

                    <div className="response-section">
                      <p className="section-label">Translation</p>
                      <p>{message.content.translation}</p>
                    </div>

                    {message.content.word_meaning ? (
                      <div className="response-section">
                        <p className="section-label">Word Meaning</p>
                        <p>{message.content.word_meaning}</p>
                      </div>
                    ) : null}

                    <div className="response-section">
                      <p className="section-label">Advice</p>
                      <p>{message.content.advice}</p>
                    </div>

                    {message.content.transaction_hash ? (
                      <div className="chain-row">
                        <span>Tx: {shortenValue(message.content.transaction_hash)}</span>
                      </div>
                    ) : null}
                  </div>
                </article>
              )
            )}

            {isLoading ? (
              <article className="message-row assistant-row">
                <div className="assistant-card loading-card">
                  <div className="loading-dots">
                    <span />
                    <span />
                    <span />
                  </div>
                  <p>Consulting the Gita and shaping a response...</p>
                </div>
              </article>
            ) : null}
          </div>

          <form className="composer" onSubmit={handleSubmit}>
            <textarea
              value={input}
              onChange={(event) => setInput(event.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Share what is weighing on you..."
              rows={3}
            />

            <div className="composer-footer">
              <p className="composer-hint">
                Supports English, Hindi, Telugu, and Kannada with word-by-word Sanskrit learning.
              </p>
              <button type="submit" className="send-button" disabled={isLoading}>
                {isLoading ? "Sending..." : "Send"}
              </button>
            </div>
          </form>

          {error ? <p className="error-banner">{error}</p> : null}
        </section>
      </main>
    </div>
  );
}

function shortenValue(value = "") {
  if (!value || value.length < 18) {
    return value;
  }
  return `${value.slice(0, 10)}...${value.slice(-6)}`;
}

export default App;
