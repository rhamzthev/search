CREATE TABLE pages (
    id SERIAL PRIMARY KEY,
    url TEXT UNIQUE NOT NULL,
    title TEXT,
    description TEXT,
    content TEXT,
    last_crawled TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE keywords (
    id SERIAL PRIMARY KEY,
    word TEXT UNIQUE NOT NULL
);

CREATE TABLE keyword_pages (
    keyword_id INTEGER REFERENCES keywords(id),
    page_id INTEGER REFERENCES pages(id),
    frequency INTEGER NOT NULL DEFAULT 1,
    PRIMARY KEY (keyword_id, page_id)
);

-- Create indexes for better performance
CREATE INDEX idx_pages_url ON pages(url);
CREATE INDEX idx_keywords_word ON keywords(word);
CREATE INDEX idx_keyword_pages_frequency ON keyword_pages(frequency);
