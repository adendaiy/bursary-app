

// import React, { useState } from 'react';
// import './App.css';
// import 'bootstrap/dist/css/bootstrap.min.css';  // Bootstrap import
// import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';  // Importing React Router components
// import CustomNavbar from './Navbar';  // Import the Navbar component
// import Footer from './Footer'; // Adjust the path as necessary
// import ApplyForBursary from './ApplyForBursary';  // Import ApplyForBursary component
// import AboutUs from './AboutUs';
// import Achievements from './Achievements';
// import HomePage from './HomePage';

// import Login from './Login';  // Import Login component
// // import Signup from './Signup';  // Import Signup component
// import Profile from './Profile';  // Import Profile component (for logged-in users)
// import Registration from './Registration';
// import ApplicantDashboard from "./ApplicantDashboard";
// import AdminDashboard from './Admin/AdminDashboard';
// import AdminAchievements from "./Admin/AdminAchievements";
// import HeroSection from './Herosection';

// // App component
// function App() {
//   // State to manage authentication status
//   const [isAuthenticated, setIsAuthenticated] = useState(false);
//   const [user, setUser] = useState(null); // Store user info when logged in

//   // Function to handle login (you will call this after successful login)
//   const handleLogin = (userData) => {
//     setIsAuthenticated(true);
//     setUser(userData);  // Set user information
//   };

//   // Function to handle logout
//   const handleLogout = () => {
//     setIsAuthenticated(false);
//     setUser(null);
//   };

//   return (
//     <Router>
//       <div className="container-fluid">
//         {/* Include the Navbar at the top, passing login/logout state and handlers */}
//         <CustomNavbar isAuthenticated={isAuthenticated} user={user} handleLogout={handleLogout} />

//         {/* Routing for different components */}
//         <Routes>
//           {/* Default route - Home Page */}
//           <Route path="/" element={<HomePage />} />
          

//           {/* Apply For Bursary Page Route */}
//           <Route path="/apply-for-bursary" element={<ApplyForBursary />} />
          
//           {/* Other Routes */}
//           <Route path="/about" element={<AboutUs />} />
//           <Route path="/achievements" element={<Achievements />} />
//           <Route path="/profile" element={<Profile />} />
        
//           <Route path="/Registration" element={<Registration />} />
//           <Route path="/register" element={<Registration />} />
//           <Route path="/login" element={<Login />} />
//           <Route path="/ApplicantDashboard" element={<ApplicantDashboard />} />

//           <Route path="/AdminDashboard" element={<AdminDashboard />} />
//           <Route path="/admin/achievements" element={<AdminAchievements />} />  {/* Admin Achievements route */}

//           {/* Login and Signup Routes */}
//           <Route path="/login" element={<Login onLogin={handleLogin} />} />  {/* Pass handleLogin to Login component */}

//           {/* Profile Route (only accessible when logged in) */}
//           {isAuthenticated && (
//             <Route path="/profile" element={<Profile user={user} />} />  // Show profile page for logged-in users
//           )}
//         </Routes>
//         <HeroSection />
//         {/* Footer */}
//         <Footer />
//       </div>
//     </Router>
//   );
// }

// export default App;



// import React, { useState } from 'react';
// import './App.css';
// import 'bootstrap/dist/css/bootstrap.min.css';  // Bootstrap import
// import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';  // Importing React Router components
// import CustomNavbar from './Navbar';  // Import the Navbar component
// import Footer from './Footer'; // Adjust the path as necessary
// import ApplyForBursary from './ApplyForBursary';  // Import ApplyForBursary component
// import AboutUs from './AboutUs';
// import Achievements from './Achievements';
// import HomePage from './HomePage';
// import Login from './Login';  // Import Login component
// import Profile from './Profile';  // Import Profile component (for logged-in users)
// import Registration from './Registration';
// import ApplicantDashboard from "./ApplicantDashboard";
// import AdminDashboard from './Admin/AdminDashboard';
// import AdminAchievements from "./Admin/AdminAchievements";
// import HeroSection from './Herosection';  // Import HeroSection component

// // App component
// function App() {
//   // State to manage authentication status
//   const [isAuthenticated, setIsAuthenticated] = useState(false);
//   const [user, setUser] = useState(null); // Store user info when logged in

//   // Function to handle login (you will call this after successful login)
//   const handleLogin = (userData) => {
//     setIsAuthenticated(true);
//     setUser(userData);  // Set user information
//   };

//   // Function to handle logout
//   const handleLogout = () => {
//     setIsAuthenticated(false);
//     setUser(null);
//   };

//   return (
//     <Router>
//       <div className="container-fluid">
//         {/* Include the Navbar at the top, passing login/logout state and handlers */}
//         <CustomNavbar isAuthenticated={isAuthenticated} user={user} handleLogout={handleLogout} />

//         {/* Using the useLocation hook inside the Router */}
//         <LocationBasedHero />

//         {/* Routing for different components */}
//         <Routes>
//           {/* Default route - Home Page */}
//           <Route path="/" element={<HomePage />} />
          
//           {/* Apply For Bursary Page Route */}
//           <Route path="/apply-for-bursary" element={<ApplyForBursary />} />
          
//           {/* Other Routes */}
//           <Route path="/about" element={<AboutUs />} />
//           <Route path="/achievements" element={<Achievements />} />
//           <Route path="/profile" element={<Profile />} />
        
//           <Route path="/Registration" element={<Registration />} />
//           <Route path="/register" element={<Registration />} />
//           <Route path="/login" element={<Login />} />
//           <Route path="/ApplicantDashboard" element={<ApplicantDashboard />} />

//           <Route path="/AdminDashboard" element={<AdminDashboard />} />
//           <Route path="/admin/achievements" element={<AdminAchievements />} />  {/* Admin Achievements route */}

//           {/* Login and Signup Routes */}
//           <Route path="/login" element={<Login onLogin={handleLogin} />} />  {/* Pass handleLogin to Login component */}

//           {/* Profile Route (only accessible when logged in) */}
//           {isAuthenticated && (
//             <Route path="/profile" element={<Profile user={user} />} />  // Show profile page for logged-in users
//           )}
//         </Routes>

//         {/* Footer */}
//         <Footer />
//       </div>
//     </Router>
//   );
// }

// // Location-based rendering of HeroSection
// function LocationBasedHero() {
//   const location = useLocation();  // Use the location hook to check the route

//   return (
//     location.pathname === "/" && <HeroSection />
//   );
// }

// export default App;




// import React, { useState } from "react";
// import "./App.css";
// import "bootstrap/dist/css/bootstrap.min.css"; // Bootstrap import
// import { BrowserRouter as Router, Routes, Route, useLocation } from "react-router-dom"; // Importing React Router components
// import CustomNavbar from "./Navbar"; // Import the Navbar component
// import Footer from "./Footer"; // Adjust the path as necessary
// import ApplyForBursary from "./ApplyForBursary"; // Import ApplyForBursary component
// import AboutUs from "./AboutUs";
// import Achievements from "./Achievements";
// import HomePage from "./HomePage";
// import Login from "./Login"; // Import Login component
// import Profile from "./Profile"; // Import Profile component (for logged-in users)
// import Registration from "./Registration";
// import ApplicantDashboard from "./ApplicantDashboard";
// import AdminDashboard from "./Admin/AdminDashboard";
// import AdminAchievements from "./Admin/AdminAchievements";
// import HeroSection from "./Herosection"; // Import HeroSection component
// import ProtectedRoute from "./ProtectedRoute"; // Import the ProtectedRoute component

// // App component
// function App() {
//   const [isAuthenticated, setIsAuthenticated] = useState(false);
//   const [user, setUser] = useState(null); // Store user info when logged in

//   // Function to handle login (you will call this after successful login)
//   const handleLogin = (userData) => {
//     setIsAuthenticated(true);
//     setUser(userData); // Set user information
//   };

//   // Function to handle logout
//   const handleLogout = () => {
//     setIsAuthenticated(false);
//     setUser(null);
//   };

//   return (
//     <Router>
//       <div className="container-fluid">
//         {/* Include the Navbar at the top, passing login/logout state and handlers */}
//         <CustomNavbar isAuthenticated={isAuthenticated} user={user} handleLogout={handleLogout} />

//         {/* Using the useLocation hook inside the Router */}
//         <LocationBasedHero />

//         {/* Routing for different components */}
//         <Routes>
//           {/* Default route - Home Page */}
//           <Route path="/" element={<HomePage />} />

//           {/* Apply For Bursary Page Route */}
//           <Route path="/apply-for-bursary" element={<ApplyForBursary />} />

//           {/* Other Routes */}
//           <Route path="/about" element={<AboutUs />} />
//           <Route path="/achievements" element={<Achievements />} />
//           <Route path="/profile" element={<Profile />} />
//           <Route path="/Registration" element={<Registration />} />
//           <Route path="/register" element={<Registration />} />
//           <Route path="/login" element={<Login onLogin={handleLogin} />} />

//           {/* Protected Route for ApplicantDashboard */}
//           <Route
//             path="/ApplicantDashboard"
//             element={
//               <ProtectedRoute isAuthenticated={isAuthenticated}>
//                 <ApplicantDashboard />
//               </ProtectedRoute>
//             }
//           />

//           {/* Protected Route for AdminDashboard */}
//           <Route
//             path="/AdminDashboard"
//             element={
//               <ProtectedRoute isAuthenticated={isAuthenticated}>
//                 <AdminDashboard />
//               </ProtectedRoute>
//             }
//           />

//           <Route path="/admin/achievements" element={<AdminAchievements />} />
//         </Routes>

//         {/* Footer */}
//         <Footer />
//       </div>
//     </Router>
//   );
// }

// // Location-based rendering of HeroSection
// function LocationBasedHero() {
//   const location = useLocation(); // Use the location hook to check the route

//   return location.pathname === "/" && <HeroSection />;
// }

// export default App;



import React, { useState } from "react";
import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import { BrowserRouter as Router, Routes, Route, useLocation } from "react-router-dom";
import CustomNavbar from "./Navbar";
import Footer from "./Footer";
import ApplyForBursary from "./ApplyForBursary";
import AboutUs from "./AboutUs";
import Achievements from "./Achievements";
import HomePage from "./HomePage";
import Login from "./Login";
import Profile from "./Profile";
import Registration from "./Registration";
import ApplicantDashboard from "./ApplicantDashboard";
import AdminDashboard from "./Admin/AdminDashboard";
import AdminAchievements from "./Admin/AdminAchievements";
import HeroSection from "./Herosection";
import ProtectedRoute from "./ProtectedRoute";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);

  const handleLogin = (userData) => {
    setIsAuthenticated(true);
    setUser(userData);
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setUser(null);
  };

  return (
    <Router>
      <div className="container-fluid">
        <CustomNavbar isAuthenticated={isAuthenticated} user={user} handleLogout={handleLogout} />
        <LocationBasedHero />

        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/apply-for-bursary" element={<ApplyForBursary />} />
          <Route path="/about" element={<AboutUs />} />
          <Route path="/achievements" element={<Achievements />} />
          <Route path="/profile" element={<Profile />} />

          <Route path="/Registration" element={<Registration />} /> 
          <Route path="/login" element={<Login onLogin={handleLogin} />} />
          
          {/* Protected Routes */}
          <Route
            path="/ApplicantDashboard"
            element={
              <ProtectedRoute isAuthenticated={isAuthenticated}>
                <ApplicantDashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/AdminDashboard/*"
            element={
                <AdminDashboard />
            }
          />

          <Route path="/admin/achievements" element={<AdminAchievements />} />
        </Routes>

        <Footer />
      </div>
    </Router>
  );
}

function LocationBasedHero() {
  const location = useLocation();
  return location.pathname === "/" && <HeroSection />;
}

export default App;
