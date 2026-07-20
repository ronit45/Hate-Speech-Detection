import { useState } from 'react'
import GlowCard from './GlowCard'

export default function Results({ result, complaint }) {
  const { threat_level, bns_section } = result
  const [copied, setCopied] = useState(false)

  const handleCopy = () => {
    if (complaint) {
      navigator.clipboard.writeText(complaint)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  const getThreatClass = (level) => {
    if (level === 'High') return 'risk-high'
    if (level === 'Medium') return 'risk-medium'
    return 'risk-low'
  }

  return (
    <GlowCard className="results-section animate-fade-in">
      <div className="card-header">
        <div className="header-label">
          <span className="dot-indicator active"></span>
          <h2>Analysis & Legal Report</h2>
        </div>
        <span className="stamp-badge">VERIFIED RESULT</span>
      </div>

      <div className="metrics-grid">
        {/* Threat Level */}
        <div className={`metric-card ${getThreatClass(threat_level)}`}>
          <div className="metric-header">
            <span className="metric-name">Threat Severity</span>
            <span className="metric-tag">MLP Classifier</span>
          </div>
          <div className="metric-body">
            <div className={`risk-badge ${getThreatClass(threat_level)}`}>
              <span className="pulse-dot"></span>
              <span>{threat_level.toUpperCase()} RISK</span>
            </div>
          </div>
          <div className="severity-bar-track">
            <div className={`severity-bar-progress level-${threat_level}`}></div>
          </div>
        </div>

        {/* BNS Categorization */}
        <div className="metric-card bns-card">
          <div className="metric-header">
            <span className="metric-name">Legal Categorization</span>
            <span className="metric-tag">Naive Bayes</span>
          </div>
          <div className="metric-body">
            <div className="bns-law-badge">
              <span className="law-icon">⚖️</span>
              <span>{bns_section}</span>
            </div>
          </div>
          <p className="bns-note">Mapped to Bharatiya Nyaya Sanhita (BNS) standards</p>
        </div>
      </div>
      
      {/* Official Legal Complaint Draft */}
      {complaint && (
        <div className="document-container animate-fade-in">
          <div className="document-top">
            <div className="document-title-wrap">
              <span className="document-icon">📜</span>
              <h3>Automated BNS Complaint Draft</h3>
            </div>
            <button 
              type="button" 
              className={`copy-document-btn ${copied ? 'copied-success' : ''}`}
              onClick={handleCopy}
            >
              {copied ? "✓ Copied to Clipboard" : "📋 Copy Complaint"}
            </button>
          </div>
          <div className="document-paper">
            <pre className="paper-text">{complaint}</pre>
          </div>
        </div>
      )}
    </GlowCard>
  )
}
