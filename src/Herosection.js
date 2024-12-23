



// // HeroSection.js
// import React from 'react';
// import './Herosection.css';

// const HeroSection = () => {
//   return (
//     <div className="hero-section">
//       <div className="hero-content-top">
//         <h1 className="hero-title">Welcome to Online Balambala Bursary Application</h1>
//       </div>
//       <div className="hero-content-bottom">
//         <p className="hero-subtitle">Apply for your bursary easily and securely online.</p>
//         <button className="btn btn-primary btn-lg mt-3">Apply Now</button>
//       </div>

//       {/* Left Moving Image */}
//       <div className="moving-image left">
//         <img src="/images/cdfLaunchImage.jpeg" alt="Left Image" />
        
//       </div>


//       {/* Rotating Logo */}
//       <div className="rotating-logo-container">
//         <img src="/images/balambala bursary logo.png" alt="CFD Logo" className="rotating-logo" />
//       </div>
//     </div>
//   );
// };

// export default HeroSection;



import React from 'react';
import { useNavigate } from 'react-router-dom'; // Import the useNavigate hook
import './Herosection.css';

const HeroSection = () => {
  const navigate = useNavigate(); // Initialize navigate function

  const handleApplyNowClick = () => {
    navigate('/Registration'); // Redirect to the login page
  };

  return (
    <div className="hero-section">
      <div className="hero-content-top">
        <h1 className="hero-title">Welcome to Online Balambala Bursary Application</h1>
      </div>
      <div className="hero-content-bottom">
        <p className="hero-subtitle">Apply for your bursary easily and securely online.</p>
        <button
          className="btn btn-primary btn-lg mt-3"
          onClick={handleApplyNowClick} // Add onClick handler
        >
          Apply Now
        </button>
      </div>

      {/* Left Moving Image */}
      <div className="moving-image left">
        <img src="/images/cdfLaunchImage.jpeg" alt="Left Image" />
      </div>

      {/* Rotating Logo */}
      <div className="rotating-logo-container">
        <img src="/images/balambala bursary logo.png" alt="CFD Logo" className="rotating-logo" />
      </div>
    </div>
  );
};

export default HeroSection;
