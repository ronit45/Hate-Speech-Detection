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
    
    try {
      const res = await fetch('http://localhost:8000/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
      })
      
      if (!res.ok) throw new Error("Failed to analyze text")
      
      const data = await res.json()
      setAnalysisResult(data)
      
      // Auto-generate complaint if needed
      if (data.threat_level !== 'Low') {
        const complaintRes = await fetch('http://localhost:8000/api/complaint/generate', {
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
    <div className="app-container">
      <header className="header animate-fade-in">
        <h1>CyberNyaya</h1>
        <p>Vernacular Cyber Harassment & Hate Speech Detection Engine</p>
      </header>

      <Analyzer onAnalyze={handleAnalyze} isLoading={loading} />
      
      {analysisResult && (
        <Results result={analysisResult} complaint={complaintDraft} />
      )}
    </div>
  )
}

export default App
