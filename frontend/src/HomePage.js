import React from 'react';
import { Link } from 'react-router-dom';
import './HomePage.css';

export default function HomePage() {
  return (
    <div className="home-container">
      <header className="hero">
        <h1>Rizzume</h1>
        <p className="tagline">Impress recruiters with a professional resume in minutes</p>
        <Link to="/builder" className="cta-button">Create My Resume</Link>
      </header>
      
      <section className="features">
        <div className="feature-card">
          <div className="feature-icon">
            <span role="img" aria-label="pencil">📝</span>
          </div>
          <h3>Easy to Use</h3>
          <p>Fill in your details with our intuitive editor and get a beautiful resume instantly</p>
        </div>
        
        <div className="feature-card">
          <div className="feature-icon">
            <span role="img" aria-label="briefcase">💼</span>
          </div>
          <h3>Professional Templates</h3>
          <p>Designed by HR professionals to maximize your chances of landing interviews</p>
        </div>
        
        <div className="feature-card">
          <div className="feature-icon">
            <span role="img" aria-label="lightning bolt">⚡</span>
          </div>
          <h3>Instant PDF</h3>
          <p>Download your polished resume as a PDF in seconds, ready to send to employers</p>
        </div>
      </section>
      
      <section className="steps">
        <h2>How It Works</h2>
        <div className="steps-container">
          <div className="step-card">
            <div className="step-number">1</div>
            <h3>Enter Your Details</h3>
            <p>Fill in your professional experience, education, and skills with our guided editor</p>
          </div>
          
          <div className="step-card">
            <div className="step-number">2</div>
            <h3>Review & Edit</h3>
            <p>See your resume take shape with our live preview and make adjustments as needed</p>
          </div>
          
          <div className="step-card">
            <div className="step-number">3</div>
            <h3>Download & Apply</h3>
            <p>Download your finished resume as a PDF and start applying for jobs with confidence</p>
          </div>
        </div>
      </section>
      
      <section className="testimonials">
        <h2>What Our Users Say</h2>
        <div className="testimonial-cards">
          <div className="testimonial-card">
            <p className="testimonial-text">"Thanks to Rizzume, I was able to create a professional resume in under 30 minutes. I got callbacks for 3 interviews in the first week!"</p>
            <div className="testimonial-author">
              <div className="author-avatar">JD</div>
              <div className="author-info">
                <h4>Ahmed Saeed Umar</h4>
                <p>Software Engineer</p>
              </div>
            </div>
          </div>
          
          <div className="testimonial-card">
            <p className="testimonial-text">"The templates are clean and professional. I especially loved how easy it was to customize and add my own sections."</p>
            <div className="testimonial-author">
              <div className="author-avatar">JS</div>
              <div className="author-info">
                <h4>Sandesh Kumar</h4>
                <p>Marketing Specialist</p>
              </div>
            </div>
          </div>
        </div>
      </section>
      
      <footer className="footer">
        <p>© {new Date().getFullYear()} Rizzume - All Rights Reserved</p>
        <a href="https://github.com/asadsehto" target="_blank" rel="noopener noreferrer">
          GitHub
        </a>
      </footer>
    </div>
  );
}
