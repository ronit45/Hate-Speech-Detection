import { useState } from 'react'
import GlowCard from './GlowCard'

const SAMPLE_PRESETS = [
  {
    label: "🔥 Hinglish Abusive",
    text: "Teri aukaat kya hai saale, tere ghar me ghus kar marunga"
  },
  {
    label: "⚠️ Online Harassment",
    text: "Go back to your country you don't belong here, I will leak your address"
  },
  {
    label: "✅ Safe Inquiry",
    text: "Hi, can you please share the schedule for tomorrow's meeting?"
  }
]

export default function Analyzer({ onAnalyze, isLoading }) {
  const [text, setText] = useState('')

  const handleSubmit = () => {
    if (text.trim()) {
      onAnalyze(text)
    }
  }

  return (
    <GlowCard className="input-section animate-fade-in">
      <div className="card-header">
        <div className="header-label">
          <span className="dot-indicator"></span>
          <h2>Paste Message or Post</h2>
        </div>
        <span className="character-counter">{text.length} chars</span>
      </div>

      {/* Preset Chips */}
      <div className="presets-wrapper">
        <span className="presets-title">Try real-world test cases:</span>
        <div className="chips-row">
          {SAMPLE_PRESETS.map((preset, idx) => (
            <button
              key={idx}
              type="button"
              className="preset-button"
              onClick={() => setText(preset.text)}
            >
              {preset.label}
            </button>
          ))}
        </div>
      </div>

      <div className="input-field-wrapper">
        <textarea 
          placeholder="Paste social media comment, direct message, or post here..."
          value={text}
          onChange={(e) => setText(e.target.value)}
          rows={5}
        />
        {text && (
          <button 
            type="button" 
            className="clear-icon-btn" 
            onClick={() => setText('')}
            title="Clear text"
          >
            ✕
          </button>
        )}
      </div>

      <button 
        className="main-submit-btn" 
        onClick={handleSubmit}
        disabled={isLoading || !text.trim()}
      >
        {isLoading ? (
          <div className="loading-state">
            <div className="spinner-ring"></div>
            <span>Analyzing message patterns & BNS legal sections...</span>
          </div>
        ) : (
          <div className="submit-state">
            <span>ANALYZE RISK & GENERATE BNS DRAFT</span>
            <span className="arrow-symbol">→</span>
          </div>
        )}
      </button>
    </GlowCard>
  )
}
