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
    <div className="container">
      <div className="header">
        <nav className="main-nav">
          <a href="https://linkedin.com/in/rhamzthev" target="_blank" rel="noopener noreferrer">LinkedIn</a>
          <a href="https://github.com/rhamzthev" target="_blank" rel="noopener noreferrer">GitHub</a>
          <a href="/resume" className="resume-btn">Resume</a>
        </nav>
      </div>

      <div className="search-container">
        <h1 className="logo">
          Rhamsez Thevenin
        </h1>
        <div className="search-box">
          <input
            type="text"
            value={searchQuery}
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                handleSearch()
              }
            }}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search my websites..."
          />
          <div className="search-icons">
            <span className="search-icon">🔎</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App