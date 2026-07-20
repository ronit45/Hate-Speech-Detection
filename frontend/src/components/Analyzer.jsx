import { useState } from 'react'

export default function Analyzer({ onAnalyze, isLoading }) {
  const [text, setText] = useState('')

  const handleSubmit = () => {
    if (text.trim()) {
      onAnalyze(text)
    }
  }

  return (
    <section className="panel input-section animate-fade-in" style={{ animationDelay: '0.1s' }}>
      <h2>Enter message for analysis</h2>
      <div className="textarea-container">
        <textarea 
          placeholder="Paste social media text, DM, or message here (Hinglish/English)..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
      </div>
      <button 
        className="analyze-btn" 
        onClick={handleSubmit}
        disabled={isLoading || !text.trim()}
      >
        {isLoading ? <div className="loader"></div> : "Analyze Risk Level"}
      </button>
    </section>
  )
}
