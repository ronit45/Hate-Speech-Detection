import { useState } from 'react'
import Analyzer from './components/Analyzer'
import Results from './components/Results'
import './index.css'

function App() {
  const [analysisResult, setAnalysisResult] = useState(null)
  const [complaintDraft, setComplaintDraft] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleAnalyze = async (text) => {
    setLoading(true)
    setAnalysisResult(null)
    setComplaintDraft(null)

    const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

    try {
      const res = await fetch(`${API_BASE_URL}/api/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
      })

      if (!res.ok) throw new Error("Failed to analyze text")

      const data = await res.json()
      setAnalysisResult(data)

      // Auto-generate complaint if needed
      if (data.threat_level !== 'Low') {
        const complaintRes = await fetch(`${API_BASE_URL}/api/complaint/generate`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            original_text: data.original_text,
            bns_section: data.bns_section,
            threat_level: data.threat_level
          })
        })
        const complaintData = await complaintRes.json()
        setComplaintDraft(complaintData.draft)
      }
    } catch (err) {
      console.error(err)
      alert("Error analyzing text. Ensure backend is running on port 8000.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <div className="app-container">
        <header className="header animate-fade-in">
          <div className="human-pill">
            <span className="live-dot"></span>
            <span>INDIAN CYBER LAW & HATE SPEECH SHIELD</span>
          </div>
          <h1 className="main-title">CYBERNYAYA</h1>
          <p className="main-subtitle">
            Vernacular Cyber Harassment & Hate Speech Detection Engine
          </p>
        </header>

        <main className="main-content-layout">
          <Analyzer onAnalyze={handleAnalyze} isLoading={loading} />

          {analysisResult && (
            <Results result={analysisResult} complaint={complaintDraft} />
          )}
        </main>
      </div>
    </>
  )
}

export default App
