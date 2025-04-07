export default function Preview({ formData }) {
  return (
    <div className="resume-preview">
      <div className="resume-header">
        <h2>{formData.name || 'Your Name'}</h2>
        <p>
          {formData.phone && <span>{formData.phone} • </span>}
          {formData.email || 'your@email.com'}
          {formData.linkedin && <span> • linkedin.com/in/{formData.linkedin}</span>}
          {formData.github && <span> • github.com/{formData.github}</span>}
        </p>
      </div>
      
      {/* Education Preview */}
      {formData.education.length > 0 && (
        <div className="section">
          <h3>Education</h3>
          {formData.education.map((edu, index) => (
            <div key={index} className="item">
              <div className="item-header">
                <h4>{edu.institution || 'University'}</h4>
                <span>{edu.dates || 'Dates'}</span>
              </div>
              <p>{edu.degree || 'Degree'} {edu.location && `• ${edu.location}`}</p>
            </div>
          ))}
        </div>
      )}
      
      {/* Experience Preview */}
      {formData.experience.length > 0 && (
        <div className="section">
          <h3>Experience</h3>
          {formData.experience.map((exp, index) => (
            <div key={index} className="item">
              <div className="item-header">
                <h4>{exp.position || 'Position'} at {exp.company || 'Company'}</h4>
                <span>{exp.dates || 'Dates'}</span>
              </div>
              {exp.location && <p>{exp.location}</p>}
              <ul className="bullets">
                {exp.bullets.map((bullet, bIndex) => (
                  bullet && <li key={bIndex}>{bullet}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}
      
      {/* Projects Preview */}
      {formData.projects.length > 0 && (
        <div className="section">
          <h3>Projects</h3>
          {formData.projects.map((proj, index) => (
            <div key={index} className="item">
              <div className="item-header">
                <h4>{proj.name || 'Project Name'}</h4>
                <span>{proj.dates || 'Dates'}</span>
              </div>
              {proj.technologies && <p>{proj.technologies}</p>}
              <ul className="bullets">
                {proj.bullets.map((bullet, bIndex) => (
                  bullet && <li key={bIndex}>{bullet}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}
      
      {/* Skills Preview */}
      {Object.keys(formData.skills).length > 0 && (
        <div className="section">
          <h3>Skills</h3>
          <div className="skills-grid">
            {Object.entries(formData.skills).map(([category, skills]) => (
              <div key={category} className="skill-category">
                <h4>{category}</h4>
                <ul>
                  {skills.filter(skill => skill).map((skill, index) => (
                    <li key={index}>{skill}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
