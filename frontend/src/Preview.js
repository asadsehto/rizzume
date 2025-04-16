import React from 'react';
import './Preview.css';

export default function Preview({ formData }) {
  return (
    <div className="resume-preview">
      <div className="resume-header">
        <h1>{formData.name || 'Your Name'}</h1>
        <div className="contact-info">
          {formData.phone && (
            <div className="contact-item">
              <span className="contact-icon">📱</span>
              <span>{formData.phone}</span>
            </div>
          )}
          {formData.email && (
            <div className="contact-item">
              <span className="contact-icon">✉️</span>
              <span>{formData.email}</span>
            </div>
          )}
          {formData.linkedin && (
            <div className="contact-item">
              <span className="contact-icon">🔗</span>
              <span>linkedin.com/in/{formData.linkedin}</span>
            </div>
          )}
          {formData.github && (
            <div className="contact-item">
              <span className="contact-icon">💻</span>
              <span>github.com/{formData.github}</span>
            </div>
          )}
        </div>
      </div>
      
      {/* Education Preview */}
      {formData.education.length > 0 && (
        <div className="resume-section">
          <h2 className="section-title">Education</h2>
          <div className="section-content">
            {formData.education.map((edu, index) => (
              <div key={index} className="item">
                <div className="item-header">
                  <h3 className="item-title">{edu.institution || 'University'}</h3>
                  <span className="item-date">{edu.dates || 'Dates'}</span>
                </div>
                <div className="item-subtitle">
                  <span className="degree">{edu.degree || 'Degree'}</span>
                  {edu.location && <span className="location">{edu.location}</span>}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
      
      {/* Experience Preview */}
      {formData.experience.length > 0 && (
        <div className="resume-section">
          <h2 className="section-title">Experience</h2>
          <div className="section-content">
            {formData.experience.map((exp, index) => (
              <div key={index} className="item">
                <div className="item-header">
                  <h3 className="item-title">{exp.position || 'Position'}</h3>
                  <span className="item-date">{exp.dates || 'Dates'}</span>
                </div>
                <div className="item-subtitle">
                  <span className="company">{exp.company || 'Company'}</span>
                  {exp.location && <span className="location">{exp.location}</span>}
                </div>
                <ul className="item-bullets">
                  {exp.bullets.map((bullet, bIndex) => (
                    bullet && <li key={bIndex}>{bullet}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      )}
      
      {/* Projects Preview */}
      {formData.projects.length > 0 && (
        <div className="resume-section">
          <h2 className="section-title">Projects</h2>
          <div className="section-content">
            {formData.projects.map((proj, index) => (
              <div key={index} className="item">
                <div className="item-header">
                  <h3 className="item-title">{proj.name || 'Project Name'}</h3>
                  <span className="item-date">{proj.dates || 'Dates'}</span>
                </div>
                {proj.technologies && (
                  <div className="technologies">
                    <span className="tech-label">Technologies:</span> {proj.technologies}
                  </div>
                )}
                <ul className="item-bullets">
                  {proj.bullets.map((bullet, bIndex) => (
                    bullet && <li key={bIndex}>{bullet}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      )}
      
      {/* Skills Preview */}
      {Object.keys(formData.skills).length > 0 && (
        <div className="resume-section">
          <h2 className="section-title">Skills</h2>
          <div className="skills-content">
            {Object.entries(formData.skills).map(([category, skills]) => (
              <div key={category} className="skill-category">
                <h3 className="category-title">{category}</h3>
                <div className="skills-list">
                  {skills.filter(skill => skill).map((skill, index) => (
                    <span key={index} className="skill-badge">{skill}</span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}