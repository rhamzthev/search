import styles from './Resume.module.css'

export default function Resume() {
    return (
        <div className={styles['resume-container']}>
            <header className={styles['resume-header']}>
                <a href="/" className={styles['back-link']}>
                    ← Back to Search
                </a>
                <a href="/resume.pdf" download className={styles['download-link']}>
                    Download PDF
                </a>
            </header>
            <object
                data="/resume.pdf"
                type="application/pdf"
                className={styles['resume-viewer']}
            >
                <div className={styles['fallback']}>
                    <p>Unable to display PDF file.</p>
                    <a href="/resume.pdf" download className={styles['download-link']}>
                        Download PDF
                    </a>
                </div>
            </object>
        </div>
    );
}