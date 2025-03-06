import { useState } from 'react'
import './App.css'
import { useNavigate } from 'react-router'

function App() {
  const [searchQuery, setSearchQuery] = useState('')
  const navigate = useNavigate()
  
  const handleSearch = (e?: React.FormEvent) => {
    if (e) e.preventDefault()
    if (!searchQuery.trim()) return
    navigate(`/search?q=${encodeURIComponent(searchQuery.trim())}`)
  }
  
  return (
    <div className="home-container container">
      <header className="header">
        <nav className="nav-links">
          <a href="https://linkedin.com/in/rhamzthev" target="_blank" rel="noopener noreferrer" className="nav-link">LinkedIn</a>
          <a href="https://github.com/rhamzthev" target="_blank" rel="noopener noreferrer" className="nav-link">GitHub</a>
          <a href="/resume" className="resume-link">Resume</a>
        </nav>
      </header>

      <div className="search-container">
        <h1 className="logo-title">
          Rhamsez Thevenin
        </h1>
        <div className="search-box-container">
          <form onSubmit={handleSearch}>
            <div className="search-box">
              <input
                type="text"
                className="search-input"
                value={searchQuery}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    handleSearch()
                  }
                }}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search my websites..."
              />
              <div className="search-icon" onClick={handleSearch}>
                <span>🔎</span>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}

export default App