import React, { useState } from 'react';
import './App.css';

function App() {
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    email: '',
    linkedin: '',
    github: '',
    education: [{ institution: '', location: '', degree: '', dates: '' }],
    experience: [{ position: '', company: '', location: '', dates: '', bullets: [''] }],
    projects: [{ name: '', technologies: '', dates: '', bullets: [''] }],
    skills: { 'Programming Languages': [''] }
  });
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  
  // Handle basic info changes
  const handleBasicInfoChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };
  
  // Handle education changes
  const handleEducationChange = (index, field, value) => {
    const newEducation = [...formData.education];
    newEducation[index][field] = value;
    setFormData({
      ...formData,
      education: newEducation
    });
  };
  
  // Add new education field
  const addEducation = () => {
    setFormData({
      ...formData,
      education: [...formData.education, { institution: '', location: '', degree: '', dates: '' }]
    });
  };
  
  // Remove education field
  const removeEducation = (index) => {
    const newEducation = [...formData.education];
    newEducation.splice(index, 1);
    setFormData({
      ...formData,
      education: newEducation
    });
  };
  
  // Handle experience changes
  const handleExperienceChange = (index, field, value) => {
    const newExperience = [...formData.experience];
    newExperience[index][field] = value;
    setFormData({
      ...formData,
      experience: newExperience
    });
  };
  
  // Handle experience bullet changes
  const handleBulletChange = (expIndex, bulletIndex, value) => {
    const newExperience = [...formData.experience];
    newExperience[expIndex].bullets[bulletIndex] = value;
    setFormData({
      ...formData,
      experience: newExperience
    });
  };
  
  // Add new bullet to experience
  const addBullet = (index) => {
    const newExperience = [...formData.experience];
    newExperience[index].bullets.push('');
    setFormData({
      ...formData,
      experience: newExperience
    });
  };
  
  // Remove bullet from experience
  const removeBullet = (expIndex, bulletIndex) => {
    const newExperience = [...formData.experience];
    newExperience[expIndex].bullets.splice(bulletIndex, 1);
    setFormData({
      ...formData,
      experience: newExperience
    });
  };
  
  // Add new experience
  const addExperience = () => {
    setFormData({
      ...formData,
      experience: [...formData.experience, { position: '', company: '', location: '', dates: '', bullets: [''] }]
    });
  };
  
  // Remove experience
  const removeExperience = (index) => {
    const newExperience = [...formData.experience];
    newExperience.splice(index, 1);
    setFormData({
      ...formData,
      experience: newExperience
    });
  };
  
  // Handle project changes
  const handleProjectChange = (index, field, value) => {
    const newProjects = [...formData.projects];
    newProjects[index][field] = value;
    setFormData({
      ...formData,
      projects: newProjects
    });
  };
  
  // Handle project bullet changes
  const handleProjectBulletChange = (projIndex, bulletIndex, value) => {
    const newProjects = [...formData.projects];
    newProjects[projIndex].bullets[bulletIndex] = value;
    setFormData({
      ...formData,
      projects: newProjects
    });
  };
  
  // Add new bullet to project
  const addProjectBullet = (index) => {
    const newProjects = [...formData.projects];
    newProjects[index].bullets.push('');
    setFormData({
      ...formData,
      projects: newProjects
    });
  };
  
  // Remove bullet from project
  const removeProjectBullet = (projIndex, bulletIndex) => {
    const newProjects = [...formData.projects];
    newProjects[projIndex].bullets.splice(bulletIndex, 1);
    setFormData({
      ...formData,
      projects: newProjects
    });
  };
  
  // Add new project
  const addProject = () => {
    setFormData({
      ...formData,
      projects: [...formData.projects, { name: '', technologies: '', dates: '', bullets: [''] }]
    });
  };
  
  // Remove project
  const removeProject = (index) => {
    const newProjects = [...formData.projects];
    newProjects.splice(index, 1);
    setFormData({
      ...formData,
      projects: newProjects
    });
  };
  
  // Handle skills category changes
  const handleSkillCategoryChange = (oldCategory, newCategory) => {
    const newSkills = { ...formData.skills };
    const categorySkills = newSkills[oldCategory];
    delete newSkills[oldCategory];
    newSkills[newCategory] = categorySkills;
    setFormData({
      ...formData,
      skills: newSkills
    });
  };
  
  // Handle skill changes
  const handleSkillChange = (category, index, value) => {
    const newSkills = { ...formData.skills };
    newSkills[category][index] = value;
    setFormData({
      ...formData,
      skills: newSkills
    });
  };
  
  // Add new skill to category
  const addSkill = (category) => {
    const newSkills = { ...formData.skills };
    newSkills[category].push('');
    setFormData({
      ...formData,
      skills: newSkills
    });
  };
  
  // Remove skill from category
  const removeSkill = (category, index) => {
    const newSkills = { ...formData.skills };
    newSkills[category].splice(index, 1);
    
    // If no skills left in category, remove the category
    if (newSkills[category].length === 0) {
      delete newSkills[category];
    }
    
    setFormData({
      ...formData,
      skills: newSkills
    });
  };
  
  // Add new skill category
  const addSkillCategory = () => {
    const newSkills = { ...formData.skills };
    newSkills['New Category'] = [''];
    setFormData({
      ...formData,
      skills: newSkills
    });
  };
  
  // Remove skill category
  const removeSkillCategory = (category) => {
    const newSkills = { ...formData.skills };
    delete newSkills[category];
    setFormData({
      ...formData,
      skills: newSkills
    });
  };
  
 // Complete handleSubmit function with enhanced debugging
const handleSubmit = async (e) => {
  e.preventDefault();
  setLoading(true);
  setError('');
  setSuccess(false);
  
  const BACKEND_URL = 'https://rizzume-production-388f.up.railway.app';
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 60000); // 60 seconds timeout
  
  // First check if the API is healthy
  try {
    console.log("Checking API health...");
    const healthCheck = await fetch(`${BACKEND_URL}/health`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Origin': window.location.origin,
      },
      signal: controller.signal
    }).catch(err => {
      console.error("Health check failed:", err);
      return { ok: false, status: 0, statusText: "Could not connect to server" };
    });
    
    if (!healthCheck.ok) {
      console.warn(`Health check failed with status: ${healthCheck.status}`);
      let healthData = {};
      try {
        healthData = await healthCheck.json();
        console.log("Health check details:", healthData);
      } catch (e) {
        console.error("Could not parse health check response", e);
      }
    } else {
      console.log("Health check passed");
    }
  } catch (err) {
    console.error("Error during health check:", err);
  }
  
  try {
    console.log("Sending resume data to API...");
    console.log("Form data summary:", {
      name: formData.name,
      sections: {
        education: formData.education.length,
        experience: formData.experience.length,
        projects: formData.projects.length,
        skillCategories: Object.keys(formData.skills).length
      }
    });
    
    // Make API call to backend
    const response = await fetch(`${BACKEND_URL}/generate-pdf`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Origin': window.location.origin,
      },
      body: JSON.stringify(formData),
      signal: controller.signal
    });
    
    clearTimeout(timeoutId);
    
    console.log(`Response status: ${response.status} ${response.statusText}`);
    console.log(`Response headers:`, Object.fromEntries([...response.headers.entries()]));
    
    if (!response.ok) {
      let errorMessage = `Failed to generate resume (HTTP ${response.status})`;
      let errorDetails = {};
      
      try {
        errorDetails = await response.json();
        console.error("Error details from server:", errorDetails);
        errorMessage = errorDetails.error || errorMessage;
      } catch (e) {
        console.error("Could not parse error response:", e);
        errorMessage = response.statusText || errorMessage;
      }
      
      throw new Error(`${errorMessage}${errorDetails.traceback ? '\n\nServer traceback available in console' : ''}`);
    }
    
    // Get blob from response
    const blob = await response.blob();
    console.log(`Received blob of type: ${blob.type}, size: ${blob.size} bytes`);
    
    // Check if we received a PDF
    if (blob.type !== 'application/pdf' && !blob.type.includes('pdf')) {
      console.error("Received invalid content type:", blob.type);
      
      // Try to extract text from the response for debugging
      try {
        const textResponse = await blob.text();
        console.error("Response content:", textResponse.substring(0, 1000) + (textResponse.length > 1000 ? '...' : ''));
      } catch (e) {
        console.error("Could not read response content:", e);
      }
      
      throw new Error(`Invalid response from server. Expected PDF but got ${blob.type}`);
    }
    
    // Create download link
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = 'resume.pdf';
    
    // Append to the document and trigger the download
    document.body.appendChild(a);
    a.click();
    
    // Clean up
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
    
    setSuccess(true);
  } catch (err) {
    console.error("Error generating resume:", err);
    if (err.name === 'AbortError') {
      setError('Request timed out. The server might be busy. Please try again.');
    } else {
      setError(err.message);
    }
  } finally {
    setLoading(false);
  }
};

// Complete return statement with form UI
return (
  <div className="app">
    <header className="header">
      <h1>Rizzume - Professional Resume Builder</h1>
      <p>Create a stunning professional resume in minutes</p>
    </header>
    
    <div className="container">
      <form onSubmit={handleSubmit} className="resume-form">
        <div className="section">
          <h2>Personal Information</h2>
          <div className="form-group">
            <label htmlFor="name">Full Name</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleBasicInfoChange}
              required
            />
          </div>
          
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="phone">Phone</label>
              <input
                type="tel"
                id="phone"
                name="phone"
                value={formData.phone}
                onChange={handleBasicInfoChange}
                required
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleBasicInfoChange}
                required
              />
            </div>
          </div>
          
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="linkedin">LinkedIn Username</label>
              <input
                type="text"
                id="linkedin"
                name="linkedin"
                value={formData.linkedin}
                onChange={handleBasicInfoChange}
                placeholder="yourname"
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="github">GitHub Username</label>
              <input
                type="text"
                id="github"
                name="github"
                value={formData.github}
                onChange={handleBasicInfoChange}
                placeholder="yourusername"
              />
            </div>
          </div>
        </div>
        
        <div className="section">
          <h2>Education</h2>
          {formData.education.map((edu, index) => (
            <div key={index} className="item-container">
              <div className="form-row">
                <div className="form-group">
                  <label>Institution</label>
                  <input
                    type="text"
                    value={edu.institution}
                    onChange={(e) => handleEducationChange(index, 'institution', e.target.value)}
                    required
                  />
                </div>
                
                <div className="form-group">
                  <label>Location</label>
                  <input
                    type="text"
                    value={edu.location}
                    onChange={(e) => handleEducationChange(index, 'location', e.target.value)}
                  />
                </div>
              </div>
              
              <div className="form-row">
                <div className="form-group">
                  <label>Degree</label>
                  <input
                    type="text"
                    value={edu.degree}
                    onChange={(e) => handleEducationChange(index, 'degree', e.target.value)}
                    required
                  />
                </div>
                
                <div className="form-group">
                  <label>Dates</label>
                  <input
                    type="text"
                    value={edu.dates}
                    onChange={(e) => handleEducationChange(index, 'dates', e.target.value)}
                    placeholder="May 2020 - Present"
                    required
                  />
                </div>
              </div>
              
              {formData.education.length > 1 && (
                <button
                  type="button"
                  className="remove-btn"
                  onClick={() => removeEducation(index)}
                >
                  Remove Education
                </button>
              )}
            </div>
          ))}
          
          <button
            type="button"
            className="add-btn"
            onClick={addEducation}
          >
            Add Education
          </button>
        </div>
        
        <div className="section">
          <h2>Work Experience</h2>
          {formData.experience.map((exp, index) => (
            <div key={index} className="item-container">
              <div className="form-row">
                <div className="form-group">
                  <label>Position</label>
                  <input
                    type="text"
                    value={exp.position}
                    onChange={(e) => handleExperienceChange(index, 'position', e.target.value)}
                    required
                  />
                </div>
                
                <div className="form-group">
                  <label>Dates</label>
                  <input
                    type="text"
                    value={exp.dates}
                    onChange={(e) => handleExperienceChange(index, 'dates', e.target.value)}
                    placeholder="Jan 2020 - Present"
                    required
                  />
                </div>
              </div>
              
              <div className="form-row">
                <div className="form-group">
                  <label>Company</label>
                  <input
                    type="text"
                    value={exp.company}
                    onChange={(e) => handleExperienceChange(index, 'company', e.target.value)}
                    required
                  />
                </div>
                
                <div className="form-group">
                  <label>Location</label>
                  <input
                    type="text"
                    value={exp.location}
                    onChange={(e) => handleExperienceChange(index, 'location', e.target.value)}
                  />
                </div>
              </div>
              
              <div className="bullet-points">
                <label>Bullet Points (Responsibilities & Achievements)</label>
                {exp.bullets.map((bullet, bIndex) => (
                  <div key={bIndex} className="bullet-input">
                    <input
                      type="text"
                      value={bullet}
                      onChange={(e) => handleBulletChange(index, bIndex, e.target.value)}
                      placeholder="Describe your achievement"
                      required
                    />
                    {exp.bullets.length > 1 && (
                      <button
                        type="button"
                        className="remove-bullet-btn"
                        onClick={() => removeBullet(index, bIndex)}
                      >
                        ✕
                      </button>
                    )}
                  </div>
                ))}
                <button
                  type="button"
                  className="add-bullet-btn"
                  onClick={() => addBullet(index)}
                >
                  Add Bullet Point
                </button>
              </div>
              
              {formData.experience.length > 1 && (
                <button
                  type="button"
                  className="remove-btn"
                  onClick={() => removeExperience(index)}
                >
                  Remove Experience
                </button>
              )}
            </div>
          ))}
          
          <button
            type="button"
            className="add-btn"
            onClick={addExperience}
          >
            Add Experience
          </button>
        </div>
        
        <div className="section">
          <h2>Projects</h2>
          {formData.projects.map((project, index) => (
            <div key={index} className="item-container">
              <div className="form-row">
                <div className="form-group">
                  <label>Project Name</label>
                  <input
                    type="text"
                    value={project.name}
                    onChange={(e) => handleProjectChange(index, 'name', e.target.value)}
                    required
                  />
                </div>
                
                <div className="form-group">
                  <label>Dates</label>
                  <input
                    type="text"
                    value={project.dates}
                    onChange={(e) => handleProjectChange(index, 'dates', e.target.value)}
                    placeholder="June 2023"
                  />
                </div>
              </div>
              
              <div className="form-group">
                <label>Technologies Used</label>
                <input
                  type="text"
                  value={project.technologies}
                  onChange={(e) => handleProjectChange(index, 'technologies', e.target.value)}
                  placeholder="Python, JavaScript, React"
                  required
                />
              </div>
              
              <div className="bullet-points">
                <label>Bullet Points (Project Details)</label>
                {project.bullets.map((bullet, bIndex) => (
                  <div key={bIndex} className="bullet-input">
                    <input
                      type="text"
                      value={bullet}
                      onChange={(e) => handleProjectBulletChange(index, bIndex, e.target.value)}
                      placeholder="Describe project features or your contributions"
                      required
                    />
                    {project.bullets.length > 1 && (
                      <button
                        type="button"
                        className="remove-bullet-btn"
                        onClick={() => removeProjectBullet(index, bIndex)}
                      >
                        ✕
                      </button>
                    )}
                  </div>
                ))}
                <button
                  type="button"
                  className="add-bullet-btn"
                  onClick={() => addProjectBullet(index)}
                >
                  Add Bullet Point
                </button>
              </div>
              
              {formData.projects.length > 1 && (
                <button
                  type="button"
                  className="remove-btn"
                  onClick={() => removeProject(index)}
                >
                  Remove Project
                </button>
              )}
            </div>
          ))}
          
          <button
            type="button"
            className="add-btn"
            onClick={addProject}
          >
            Add Project
          </button>
        </div>
        
        <div className="section">
          <h2>Technical Skills</h2>
          {Object.entries(formData.skills).map(([category, skills]) => (
            <div key={category} className="skill-category">
              <div className="category-header">
                <input
                  type="text"
                  value={category}
                  onChange={(e) => handleSkillCategoryChange(category, e.target.value)}
                  className="category-name"
                  placeholder="Category name"
                  required
                />
                <button
                  type="button"
                  className="remove-category-btn"
                  onClick={() => removeSkillCategory(category)}
                >
                  Remove Category
                </button>
              </div>
              
              <div className="skills-list">
                {skills.map((skill, index) => (
                  <div key={index} className="skill-input">
                    <input
                      type="text"
                      value={skill}
                      onChange={(e) => handleSkillChange(category, index, e.target.value)}
                      placeholder="Enter skill"
                      required
                    />
                    <button
                      type="button"
                      className="remove-skill-btn"
                      onClick={() => removeSkill(category, index)}
                    >
                      ✕
                    </button>
                  </div>
                ))}
                <button
                  type="button"
                  className="add-skill-btn"
                  onClick={() => addSkill(category)}
                >
                  Add Skill
                </button>
              </div>
            </div>
          ))}
          
          <button
            type="button"
            className="add-btn"
            onClick={addSkillCategory}
          >
            Add Skill Category
          </button>
        </div>
        
        {error && (
          <div className="error-message">
            <p><strong>Error:</strong> {error}</p>
            <p>Please try again or contact support if the issue persists.</p>
          </div>
        )}
        
        {success && (
          <div className="success-message">
            <p>Resume generated successfully!</p>
            <p>If the download didn't start automatically, please check your browser settings.</p>
          </div>
        )}
        
        <div className="form-actions">
          <button
            type="submit"
            className="submit-btn"
            disabled={loading}
          >
            {loading ? (
              <span>
                <span className="loading-spinner"></span>
                Generating PDF...
              </span>
            ) : (
              'Generate Resume PDF'
            )}
          </button>
        </div>
      </form>
    </div>
    
    <footer className="footer">
      <p>© {new Date().getFullYear()} Rizzume - All Rights Reserved</p>
    </footer>
  </div>
);

export default App;
