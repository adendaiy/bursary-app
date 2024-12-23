import React from 'react';
import { Container, Row, Col, Card } from 'react-bootstrap';

function Profile({ user }) {
  return (
    <Container className="mt-5">
      <Row className="justify-content-center">
        <Col md={8}>
          <Card>
            <Card.Header>
              <h3>Welcome, {user ? user.name : 'User'}!</h3>
            </Card.Header>
            <Card.Body>
              <h5>Your Profile Information</h5>
              <ul>
                <li><strong>Name:</strong> {user ? user.name : 'N/A'}</li>
                <li><strong>Email:</strong> {user ? user.email : 'N/A'}</li>
                {/* Add other user details here */}
              </ul>

              {/* If you're building a bursary system, you can show user applications */}
              <h5>Your Bursary Applications</h5>
              {/* You can render the user's bursary applications here if that data is available */}
              <ul>
                {/* Mock Example: Display some user applications or information */}
                <li>Bursary Application #1: <strong>Pending</strong></li>
              </ul>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}

export default Profile;





// import 'bootstrap/dist/css/bootstrap.min.css';

// import React, { useState, useEffect } from 'react';
// import { Container, Row, Col, Card, Form, Button, Alert, ProgressBar } from 'react-bootstrap';
// import axios from 'axios';

// function Profile() {
//   const [student, setStudent] = useState({
//     full_Name: 'Aden Daiy',
//     schoolName: 'Garissa University',
//     admissionNumber: 'GU2023001',
//     email: 'adendaiy@example.com',
//     phoneNumber: '0720123456',
//   });

//   const [hasApplied, setHasApplied] = useState(false);
//   const [bursaryStatus, setBursaryStatus] = useState(null); // Status: pending, approved, rejected
//   const [applicationData, setApplicationData] = useState({
//     familyIncome: '',
//     reason: '',
//     supportingDocuments: null,
//   });
//   const [error, setError] = useState('');
//   const [success, setSuccess] = useState('');

//   // Simulate fetching bursary application status
//   useEffect(() => {
//     // Call backend API to check if the student has already applied
//     const fetchApplicationStatus = async () => {
//       try {
//         const res = await axios.get('http://127.0.0.1:5000/bursary-status', {
//           params: { admissionNumber: student.admissionNumber },
//         });
//         if (res.data.hasApplied) {
//           setHasApplied(true);
//           setBursaryStatus(res.data.status); // pending, approved, rejected
//         }
//       } catch (err) {
//         console.log('Error fetching application status:', err);
//       }
//     };
//     fetchApplicationStatus();
//   }, [student.admissionNumber]);

//   const handleInputChange = (e) => {
//     const { name, value } = e.target;
//     setApplicationData({
//       ...applicationData,
//       [name]: value,
//     });
//   };

//   const handleFileChange = (e) => {
//     setApplicationData({
//       ...applicationData,
//       supportingDocuments: e.target.files[0],
//     });
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     // Submit bursary application
//     try {
//       const formData = new FormData();
//       formData.append('familyIncome', applicationData.familyIncome);
//       formData.append('reason', applicationData.reason);
//       formData.append('supportingDocuments', applicationData.supportingDocuments);

//       await axios.post('http://127.0.0.1:5000/apply-bursary', formData, {
//         headers: {
//           'Content-Type': 'multipart/form-data',
//         },
//       });

//       setSuccess('Bursary application submitted successfully.');
//       setHasApplied(true);
//     } catch (err) {
//       setError('Failed to submit the application.');
//     }
//   };

//   return (
//     <Container className="mt-5">
//       <Row className="justify-content-center">
//         <Col md={8}>
//           <Card className="shadow-lg p-4">
//             <Card.Body>
//               <h2 className="text-center mb-4">Student Profile</h2>
//               <Row>
//                 <Col md={6}>
//                   <p><strong>Full Name:</strong> {student.full_Name}</p>
//                   <p><strong>School Name:</strong> {student.schoolName}</p>
//                 </Col>
//                 <Col md={6}>
//                   <p><strong>Admission Number:</strong> {student.admissionNumber}</p>
//                   <p><strong>Email:</strong> {student.email}</p>
//                   <p><strong>Phone Number:</strong> {student.phoneNumber}</p>
//                 </Col>
//               </Row>

//               {/* Display Bursary Status if Already Applied */}
//               {hasApplied ? (
//                 <div className="mt-4">
//                   <h4 className="text-center mb-3">Bursary Application Status</h4>
//                   {bursaryStatus === 'pending' && (
//                     <Alert variant="info">
//                       Your bursary application is currently <strong>pending</strong>.
//                     </Alert>
//                   )}
//                   {bursaryStatus === 'approved' && (
//                     <Alert variant="success">
//                       Congratulations! Your bursary application has been <strong>approved</strong>.
//                     </Alert>
//                   )}
//                   {bursaryStatus === 'rejected' && (
//                     <Alert variant="danger">
//                       Unfortunately, your bursary application has been <strong>rejected</strong>.
//                     </Alert>
//                   )}
//                   <ProgressBar now={bursaryStatus === 'pending' ? 50 : bursaryStatus === 'approved' ? 100 : 0} />
//                 </div>
//               ) : (
//                 // Bursary Application Form for First-Time Applicants
//                 <div className="mt-4">
//                   <h4 className="text-center mb-3">Apply for Bursary</h4>
//                   {error && <Alert variant="danger">{error}</Alert>}
//                   {success && <Alert variant="success">{success}</Alert>}
//                   <Form onSubmit={handleSubmit}>
//                     <Form.Group className="mb-3" controlId="familyIncome">
//                       <Form.Label>Family Income</Form.Label>
//                       <Form.Control
//                         type="text"
//                         name="familyIncome"
//                         value={applicationData.familyIncome}
//                         onChange={handleInputChange}
//                         placeholder="Enter your family's annual income"
//                         required
//                       />
//                     </Form.Group>

//                     <Form.Group className="mb-3" controlId="reason">
//                       <Form.Label>Reason for Applying</Form.Label>
//                       <Form.Control
//                         as="textarea"
//                         name="reason"
//                         value={applicationData.reason}
//                         onChange={handleInputChange}
//                         placeholder="Explain why you are applying for the bursary"
//                         rows={3}
//                         required
//                       />
//                     </Form.Group>

//                     <Form.Group className="mb-3" controlId="supportingDocuments">
//                       <Form.Label>Supporting Documents</Form.Label>
//                       <Form.Control
//                         type="file"
//                         name="supportingDocuments"
//                         onChange={handleFileChange}
//                         required
//                       />
//                     </Form.Group>

//                     <Button variant="primary" type="submit" className="w-100">
//                       Submit Application
//                     </Button>
//                   </Form>
//                 </div>
//               )}
//             </Card.Body>
//           </Card>
//         </Col>
//       </Row>
//     </Container>
//   );
// }

// export default Profile;
