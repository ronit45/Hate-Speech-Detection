export default function Results({ result, complaint }) {
  const { threat_level, bns_section } = result

  return (
    <section className="panel animate-fade-in" style={{ animationDelay: '0.2s' }}>
      <div className="results-grid">
        <div className="result-card">
          <h3>MLP Threat Prediction</h3>
          <div className={`threat-tag threat-${threat_level}`}>
            {threat_level} Risk
          </div>
        </div>
        <div className="result-card">
          <h3>Categorization (Naive Bayes)</h3>
          <div className="bns-tag">
            {bns_section}
          </div>
        </div>
      </div>
      
      {complaint && (
        <div className="complaint-section animate-fade-in" style={{ animationDelay: '0.4s' }}>
          <h3>Automated BNS Complaint Draft</h3>
          <pre>{complaint}</pre>
        </div>
      )}
    </section>
  )
}
