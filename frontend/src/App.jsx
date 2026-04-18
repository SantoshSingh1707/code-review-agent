import { useState, useEffect } from 'react'
import axios from 'axios'

const API_URL = 'http://localhost:8002'

function App() {
  const [code, setCode] = useState('')
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [activeTab, setActiveTab] = useState('analyze')
  const [health, setHealth] = useState(null)
  const [executionResult, setExecutionResult] = useState(null)
  const [copied, setCopied] = useState(false)

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await axios.get(`${API_URL}/health`, { timeout: 3000 })
        setHealth(res.data)
      } catch {
        setHealth(null)
      }
    }
    checkHealth()
    const interval = setInterval(checkHealth, 5000)
    return () => clearInterval(interval)
  }, [])

  const handleAnalyze = async () => {
    if (!code.trim()) {
      setError('Please enter some code to analyze')
      return
    }
    setLoading(true)
    setError('')
    setResults(null)
    setExecutionResult(null)

    try {
      const res = await axios.post(`${API_URL}/analyze/paste`, { code }, { timeout: 120000 })
      setResults(res.data)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to analyze code')
    } finally {
      setLoading(false)
    }
  }

  const handleExecute = async () => {
    if (!code.trim()) {
      setError('Please enter some code to execute')
      return
    }
    setLoading(true)
    setError('')
    setResults(null)
    setExecutionResult(null)

    try {
      const res = await axios.post(`${API_URL}/execute/code`, { code }, { timeout: 30000 })
      setExecutionResult(res.data)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to execute code')
    } finally {
      setLoading(false)
    }
  }

  const copyCode = () => {
    navigator.clipboard.writeText(code)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const sampleCode = `def fibonacci(n):
    """Calculate fibonacci number"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

result = fibonacci(10)
print(f"Fibonacci(10) = {result}")`

  const getScoreClass = (score) => {
    if (score >= 8) return 'score-good'
    if (score >= 5) return 'score-medium'
    return 'score-bad'
  }

  return (
    <div className="app-container">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <div className="logo-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <polyline points="16 18 22 12 16 6"></polyline>
                <polyline points="8 6 2 12 8 18"></polyline>
              </svg>
            </div>
            <div className="logo-text">
              <h1>Code Review Agent</h1>
              <span>AI-Powered Analysis</span>
            </div>
          </div>
          <div className="status-badge">
            <span className={`status-dot ${health?.status === 'connected' ? 'status-connected' : 'status-disconnected'}`}></span>
            <span className="status-text">{health?.model || 'Offline'}</span>
          </div>
        </div>
      </header>

      {/* Main */}
      <main className="main">
        {/* Tabs */}
        <div className="tabs">
          <button
            onClick={() => setActiveTab('analyze')}
            className={`tab ${activeTab === 'analyze' ? 'tab-active' : ''}`}
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="11" cy="11" r="8"></circle>
              <path d="M21 21l-4.35-4.35"></path>
            </svg>
            Analyze
          </button>
          <button
            onClick={() => setActiveTab('execute')}
            className={`tab ${activeTab === 'execute' ? 'tab-active' : ''}`}
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <polygon points="5 3 19 12 5 21 5 3"></polygon>
            </svg>
            Execute
          </button>
        </div>

        {/* Code Input */}
        <div className="code-section">
          <div className="code-header">
            <span className="code-label">
              {activeTab === 'analyze' ? 'Paste your Python code' : 'Enter Python code to run'}
            </span>
            <div className="code-actions">
              <button onClick={() => setCode(sampleCode)} className="btn-secondary">
                Sample
              </button>
              <button onClick={copyCode} className="btn-secondary">
                {copied ? 'Copied!' : 'Copy'}
              </button>
              <button onClick={() => setCode('')} className="btn-secondary">
                Clear
              </button>
            </div>
          </div>
          <textarea
            value={code}
            onChange={(e) => setCode(e.target.value)}
            placeholder="# Type or paste your Python code here..."
            className="input-field code-editor"
            spellCheck="false"
          />
        </div>

        {/* Action */}
        <div className="action-section">
          {activeTab === 'analyze' ? (
            <button
              onClick={handleAnalyze}
              disabled={loading || !code.trim()}
              className="btn-primary"
            >
              {loading ? (
                <>
                  <svg className="animate-spin" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <circle cx="12" cy="12" r="10" strokeOpacity="0.25"></circle>
                    <path d="M12 2a10 10 0 0 1 10 10" strokeLinecap="round"></path>
                  </svg>
                  Analyzing...
                </>
              ) : (
                <>
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
                    <path d="M2 17l10 5 10-5"></path>
                    <path d="M2 12l10 5 10-5"></path>
                  </svg>
                  Analyze Code
                </>
              )}
            </button>
          ) : (
            <button
              onClick={handleExecute}
              disabled={loading || !code.trim()}
              className="btn-primary"
            >
              {loading ? (
                <>
                  <svg className="animate-spin" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <circle cx="12" cy="12" r="10" strokeOpacity="0.25"></circle>
                    <path d="M12 2a10 10 0 0 1 10 10" strokeLinecap="round"></path>
                  </svg>
                  Running...
                </>
              ) : (
                <>
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <polygon points="5 3 19 12 5 21 5 3"></polygon>
                  </svg>
                  Execute Code
                </>
              )}
            </button>
          )}
        </div>

        {/* Error */}
        {error && (
          <div className="error-box">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="8" x2="12" y2="12"></line>
              <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
            <span>{error}</span>
          </div>
        )}

        {/* Analysis Results */}
        {results && activeTab === 'analyze' && (
          <div className="results">
            {/* Score */}
            <div className="card result-score">
              <div className="score-display">
                <div className={`score-number ${getScoreClass(results.overall_score)}`}>
                  {results.overall_score}
                  <span className="score-max">/10</span>
                </div>
                <div className="score-label">Code Score</div>
              </div>
              <div className="score-summary">
                <h3>Summary</h3>
                <p>{results.summary}</p>
              </div>
            </div>

            {/* Issues */}
            {(results.bugs?.length > 0 || results.security?.length > 0 || results.performance?.length > 0 || results.code_quality?.length > 0) && (
              <div className="issues-grid">
                {results.bugs?.length > 0 && (
                  <div className="card issue-section">
                    <div className="issue-header issue-bugs">
                      <span className="issue-icon">🐛</span>
                      <span>Bugs Found</span>
                      <span className="issue-count">{results.bugs.length}</span>
                    </div>
                    <div className="issue-list">
                      {results.bugs.map((item, i) => (
                        <div key={i} className="issue-item issue-bugs">
                          <div className="issue-desc">{item.description}</div>
                          {item.suggestion && <div className="issue-fix">→ {item.suggestion}</div>}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {results.security?.length > 0 && (
                  <div className="card issue-section">
                    <div className="issue-header issue-security">
                      <span className="issue-icon">🔒</span>
                      <span>Security</span>
                      <span className="issue-count">{results.security.length}</span>
                    </div>
                    <div className="issue-list">
                      {results.security.map((item, i) => (
                        <div key={i} className="issue-item issue-security">
                          <div className="issue-desc">{item.description}</div>
                          {item.suggestion && <div className="issue-fix">→ {item.suggestion}</div>}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {results.performance?.length > 0 && (
                  <div className="card issue-section">
                    <div className="issue-header issue-performance">
                      <span className="issue-icon">⚡</span>
                      <span>Performance</span>
                      <span className="issue-count">{results.performance.length}</span>
                    </div>
                    <div className="issue-list">
                      {results.performance.map((item, i) => (
                        <div key={i} className="issue-item issue-performance">
                          <div className="issue-desc">{item.description}</div>
                          {item.suggestion && <div className="issue-fix">→ {item.suggestion}</div>}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {results.code_quality?.length > 0 && (
                  <div className="card issue-section">
                    <div className="issue-header issue-quality">
                      <span className="issue-icon">💎</span>
                      <span>Code Quality</span>
                      <span className="issue-count">{results.code_quality.length}</span>
                    </div>
                    <div className="issue-list">
                      {results.code_quality.map((item, i) => (
                        <div key={i} className="issue-item issue-quality">
                          <div className="issue-desc">{item.description}</div>
                          {item.suggestion && <div className="issue-fix">→ {item.suggestion}</div>}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Best Practices */}
            {results.best_practices?.length > 0 && (
              <div className="card issue-section">
                <div className="issue-header issue-best">
                  <span className="issue-icon">✨</span>
                  <span>Best Practices</span>
                  <span className="issue-count">{results.best_practices.length}</span>
                </div>
                <div className="issue-list">
                  {results.best_practices.map((item, i) => (
                    <div key={i} className="issue-item issue-best">
                      <div className="issue-desc">{item.suggestion}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Execution Results */}
        {executionResult && activeTab === 'execute' && (
          <div className="card execution-result">
            <div className={`execution-status ${executionResult.success ? 'success' : 'error'}`}>
              <span className={`status-dot ${executionResult.success ? 'status-connected' : 'status-disconnected'}`}></span>
              <span>{executionResult.success ? 'Execution Successful' : 'Execution Failed'}</span>
            </div>

            {executionResult.output && (
              <div className="output-section">
                <div className="output-label">Output</div>
                <pre className="output-box output-success">{executionResult.output}</pre>
              </div>
            )}

            {executionResult.error && (
              <div className="output-section">
                <div className="output-label">Error</div>
                <pre className="output-box output-error">{executionResult.error}</pre>
              </div>
            )}
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="footer">
        <span>Code Review Agent</span>
        <span className="divider">•</span>
        <span>Powered by Ollama</span>
      </footer>
    </div>
  )
}

export default App