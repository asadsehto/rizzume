import { Link } from 'react-router-dom';
import './HomePage.css';

export default function HomePage() {
  return (
    <div className="home-container">
      <header className="hero">
        <h1>Rizzume</h1>
        <p className="tagline">Rizz the recruiter with your resume</p>
        <Link to="/builder" className="cta-button">Create My Resume</Link>
      </header>

      <section className="features">
        <div className="feature-card">
          <h3>Easy to Use</h3>
          <p>Fill in your details and get a beautiful resume instantly</p>
        </div>
        <div className="feature-card">
          <h3>Professional</h3>
          <p>Designed to impress recruiters</p>
        </div>
      </section>

      <footer className="footer">
        <p>Created by Asad Saleem</p>
        <a href="https://github.com/asadsehto" target="_blank" rel="noopener noreferrer">
          GitHub
        </a>
      </footer>
    </div>
  );
}
