export default function Preview({ formData }) {
  return (
    <div className="resume-preview">
      <div className="resume-header">
        <h2>{formData.name || 'Your Name'}</h2>
        <p>
          {formData.phone && <span>{formData.phone} • </span>}
          {formData.email || 'your@email.com'}
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
              <p>{edu.degree || 'Degree'}</p>
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
              <ul className="bullets">
                {exp.bullets.map((bullet, bIndex) => (
                  <li key={bIndex}>{bullet || 'Achievement description'}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
