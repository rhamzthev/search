import { useState, useEffect } from 'react'
import { useSearchParams, Link, useNavigate } from 'react-router'
import styles from './Search.module.css'

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
    <div className={`${styles['search-page']} container`}>
      <header className={styles['search-header']}>
        <div className={styles['header-content']}>
          <Link to="/" className={styles['logo-link']}>Rhamsez Thevenin</Link>

          <form onSubmit={handleSearch} className={styles['search-form']}>
            <div className={styles['search-box']}>
              <input
                type="text"
                className={styles['search-input']}
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search my websites..."
                aria-label="Search query"
                autoFocus={!query}
              />
              <button type="submit" className={styles['search-button']} aria-label="Search">
                <span>🔍</span>
              </button>
            </div>
          </form>

          <nav className={styles['nav-links']}>
            <a href="https://linkedin.com/in/rhamzthev" target="_blank" rel="noopener noreferrer" className={styles['nav-link']}>LinkedIn</a>
            <a href="https://github.com/rhamzthev" target="_blank" rel="noopener noreferrer" className={styles['nav-link']}>GitHub</a>
            <a href="/resume" className={styles['resume-link']}>Resume</a>
          </nav>
        </div>
      </header>

      <main className={styles['search-results']}>
        {loading ? (
          <div className={styles['loading']}>
            <div className={styles['spinner']}></div>
            <p>Searching...</p>
          </div>
        ) : (
          <>
            {query && (
              results.length > 0 ? (
                <>
                  <div className={styles['results-info']}>
                    <p>About {results.length} results for "<strong>{query}</strong>"</p>
                  </div>
                  <div className={styles['results-list']}>
                    {results.map((result) => (
                      <article key={result.id} className={styles['result-item']}>
                        <a href={result.url} target="_blank" rel="noopener noreferrer" className={styles['result-url']}>
                          {result.url}
                        </a>
                        <h3>
                          <a href={result.url} target="_blank" rel="noopener noreferrer" className={styles['result-title']}>
                            {result.title}
                          </a>
                        </h3>
                        <p className={styles['result-description']}>{result.description}</p>
                      </article>
                    ))}
                  </div>
                </>
              ) : (
                <div className={styles['no-results']}>
                  <h2>No results found for "<strong>{query}</strong>"</h2>
                  <p>Try different keywords or check your spelling.</p>
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