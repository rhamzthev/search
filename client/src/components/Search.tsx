import { useState, useEffect } from 'react'
import { useSearchParams, Link, useNavigate } from 'react-router'
import './Search.css'

interface SearchResult {
  id: number
  url: string
  title: string
  description: string
  score: number
}

function Search() {
  const [searchParams] = useSearchParams()
  const query = searchParams.get('q') || ''
  const [searchQuery, setSearchQuery] = useState(query)
  const [results, setResults] = useState<SearchResult[]>([])
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  useEffect(() => {
    if (!query) return

    // Mock data for now - this would be replaced with actual API call
    setLoading(true)
    fetch(`/api/search?q=${query}`)
      .then(res => res.json())
      .then(data => {
        setResults(data)
      }).finally(() => {
        setLoading(false)
      })
      
  }, [query])

  const handleSearch = (e?: React.FormEvent) => {
    if (e) e.preventDefault()
    if (!searchQuery.trim()) return
    navigate(`/search?q=${encodeURIComponent(searchQuery.trim())}`)
  }

  return (
    <div className="search-page">
      <header className="search-header">
        <div className="header-content">
          <Link to="/" className="logo-small">Rhamsez Thevenin</Link>

          <form onSubmit={handleSearch} className="search-form">
            <div className="search-box">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search my websites..."
                aria-label="Search query"
                autoFocus={!query}
              />
              <button type="submit" className="search-button" aria-label="Search">
                <span className="search-icon">🔍</span>
              </button>
            </div>
          </form>

          <nav className="main-nav">
            <a href="https://linkedin.com/in/rhamzthev" target="_blank" rel="noopener noreferrer">LinkedIn</a>
            <a href="https://github.com/rhamzthev" target="_blank" rel="noopener noreferrer">GitHub</a>
            <a href="/resume" className="resume-btn">Resume</a>
          </nav>
        </div>
      </header>

      <main className="search-results-container">
        {loading ? (
          <div className="loading-indicator">
            <div className="spinner"></div>
            <p>Searching...</p>
          </div>
        ) : (
          <>
            {query && (
              results.length > 0 ? (
                <>
                  <div className="results-info">
                    <p>About {results.length} results for "<strong>{query}</strong>"</p>
                  </div>
                  <div className="results-list">
                    {results.map((result) => (
                      <article key={result.id} className="result-item">
                        <a href={result.url} target="_blank" rel="noopener noreferrer" className="result-url">
                          {result.url}
                        </a>
                        <h3><a href={result.url} target="_blank" rel="noopener noreferrer" className="result-title" style={{textOverflow: 'ellipsis', whiteSpace: 'nowrap', overflow: 'hidden', display: 'block'}}>{result.title}</a></h3>
                        <p className="result-description">{result.description}</p>
                      </article>
                    ))}
                  </div>
                </>
              ) : (
                <div className="results-info">
                  <div className="no-results">
                    <h2>No results found for "<strong>{query}</strong>"</h2>
                    <p>Try different keywords or check your spelling.</p>
                  </div>
                </div>
              )
            )}
          </>
        )}
      </main>
    </div>
  )
}

export default Search 