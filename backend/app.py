
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from flask_cors import CORS
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, JWTManager
from datetime import timedelta
from marshmallow import pre_load, post_load
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message


# Initialize Flask app
app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Configure CORS to allow requests from specific origins
CORS(app, origins=["http://localhost:3000"], methods=["GET", "POST", "PUT", "DELETE"])

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'public/images'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'jfif'}
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB


# Load the secret key from an environment variable for better security
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "your_secret_key")  # Ensure to set this in your environment
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)  # Set token expiration time

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'adenabdib.com'
app.config['MAIL_PASSWORD'] = 'pbhwyziglzyipxix'

mail = Mail(app)

# Initialize extensions
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# -------------------- Models --------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    admission_number = db.Column(db.String(20), nullable=False, unique=True)
    institution_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(200), nullable=False)


class Achievement(db.Model):
    __tablename__ = 'achievements'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(255), nullable=False)
    icon = db.Column(db.String(50), nullable=True)

# -------------------- Schemas --------------------
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ('password',)  # Do not expose password in API responses

# Initialize schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)



# reject or approve for admin
# Helper Functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def send_status_update_email(email, status, comments=None):
    try:
        if status == 'pending':
            subject = 'Bursary Application Received'
            body = f'''
            Dear Applicant,

            We have received your bursary application and it is currently under review. 
            Our team will assess your application and get back to you soon.

            Application Status: Pending
            '''
        elif status == 'approved':
            subject = 'Bursary Application Approved'
            body = f'''
            Dear Applicant,

            We are pleased to inform you that your bursary application has been APPROVED.

            Application Status: Approved
            {f"Reviewer Comments: {comments}" if comments else ""}

            Next steps will be communicated separately.

            Congratulations!
            Bursary Committee
            '''
        elif status == 'rejected':
            subject = 'Bursary Application Status'
            body = f'''
            Dear Applicant,

            After careful review, we regret to inform you that your bursary application 
            has been REJECTED.

            Application Status: Rejected
            {f"Reviewer Comments: {comments}" if comments else ""}

            We appreciate your application and encourage you to apply again in the future.

            Bursary Committee
            '''
        else:
            return False

        msg = Message(
            subject=subject,
            recipients=[email],
            body=body
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False



# -------------------- Routes --------------------
@app.route('/register', methods=['POST'])
def register():
    """
    Handle user registration.
    """
    data = request.get_json()
    full_name = data.get('full_name')
    admission_number = data.get('admission_number')
    institution_name = data.get('institution_name')
    email = data.get('email')
    phone_number = data.get('phone_number')
    password = data.get('password')

    # Check if the user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'User already exists'}), 400

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Create a new user instance
    new_user = User(
        full_name=full_name,
        admission_number=admission_number,
        institution_name=institution_name,
        email=email,
        phone_number=phone_number,
        password=hashed_password
    )

    # Save the user to the database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


@app.route('/auth/login', methods=['POST'])
def login():
    """
    Handle user login and issue a JWT token.
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Find the user by email
    user = User.query.filter_by(email=email).first()



    user_data = {
        'id': user.id,
        'email': user.email,
        'phone_number':user.phone_number,
        "full_name":user.full_name,
        "admission_number":user.admission_number,
        "institution_name":user.institution_name,
    }

    # Verify password
    if user and bcrypt.check_password_hash(user.password, password):
        # Generate a JWT token
        access_token = create_access_token(identity=user.id)
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user_data': user_data
        }), 200

    return jsonify({'error': 'Invalid credentials'}), 401


@app.route('/auth/user', methods=['GET'])
@jwt_required()
def get_user_details():
    """
    Fetch authenticated user details using the JWT token.
    """
    user_id = get_jwt_identity()  # Get the user ID from the JWT token
    user = User.query.get(user_id)  # Fetch user details from the database

    if not user:
        return {"error": "User not found"}, 404

    return user_schema.dump(user), 200


# the start of the bursary application functionality


# Image upload configuration
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Database Model
class Applicant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    admission = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    form = db.Column(db.String(10), nullable=False)
    dob = db.Column(db.String(10), nullable=False)
    national_id = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    institution_type = db.Column(db.String(50), nullable=False)
    institution_name = db.Column(db.String(100), nullable=False)
    index_number = db.Column(db.String(50), nullable=True)
    constituency = db.Column(db.String(100), nullable=False)
    ward = db.Column(db.String(100), nullable=False)
    id_document = db.Column(db.String(200), nullable=True)
    birth_certificate = db.Column(db.String(200), nullable=True)
    status = db.Column(db.String(10), default="Pending")  # Status for admin to approve/reject

# Marshmallow Schema
class ApplicantSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Applicant

    @pre_load
    def format_data(self, data, **kwargs):
        return {
            'full_name': data.get('fullName'),
            'admission': data.get('admission'),
            'gender': data.get('gender'),
            'form': data.get('form'),
            'dob': data.get('dob'),
            'national_id': data.get('nationalID'),
            'phone_number': data.get('phoneNumber'),
            'email': data.get('email'),
            'institution_type': data.get('institutionType'),
            'institution_name': data.get('institutionName'),
            'index_number': data.get('indexNumber', ''),
            'constituency': data.get('constituency'),
            'ward': data.get('ward'),
            'id_document': data.get('idDocument'),
            'birth_certificate': data.get('birthCertificate'),
        }

    @post_load
    def format_response(self, data, **kwargs):
        return {
            'fullName': data['full_name'],
            'admission': data['admission'],
            'gender': data['gender'],
            'form': data['form'],
            'dob': data['dob'],
            'nationalID': data['national_id'],
            'phoneNumber': data['phone_number'],
            'email': data['email'],
            'institutionType': data['institution_type'],
            'institutionName': data['institution_name'],
            'indexNumber': data.get('index_number', ''),
            'constituency': data['constituency'],
            'ward': data['ward'],
            'idDocument': data.get('id_document'),
            'birthCertificate': data.get('birth_certificate'),
            'status': data['status'],
        }

# Initialize applicant schema
applicant_schema = ApplicantSchema()
applicants_schema = ApplicantSchema(many=True)

# Create the database tables if they do not exist
with app.app_context():
    db.create_all()

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to create a new application (with file uploads)
@app.route('/apply', methods=['POST'])
def apply_for_bursary():
    data = request.form
    errors = applicant_schema.validate(data)
    if errors:
        return jsonify(errors), 400


    # Handle file uploads
    id_document_file = request.files.get('idDocument')
    birth_certificate_file = request.files.get('birthCertificate')

    id_document_filename = ''
    birth_certificate_filename = ''

    if id_document_file and allowed_file(id_document_file.filename):
        id_document_filename = secure_filename(id_document_file.filename)
        id_document_file.save(os.path.join(app.config['UPLOAD_FOLDER'], id_document_filename))

    if birth_certificate_file and allowed_file(birth_certificate_file.filename):
        birth_certificate_filename = secure_filename(birth_certificate_file.filename)
        birth_certificate_file.save(os.path.join(app.config['UPLOAD_FOLDER'], birth_certificate_filename))

    new_applicant = Applicant(
        full_name=data['fullName'],
        admission=data['admission'],
        gender=data['gender'],
        form=data['form'],
        dob=data['dob'],
        national_id=data['nationalID'],
        phone_number=data['phoneNumber'],
        email=data['email'],
        institution_type=data['institutionType'],
        institution_name=data['institutionName'],
        index_number=data.get('indexNumber', ''),
        constituency=data['constituency'],
        ward=data['ward'],
        id_document=f'http://localhost:5000/uploads/{id_document_filename}' if id_document_filename else None,
        birth_certificate=f'http://localhost:5000/uploads/{birth_certificate_filename}' if birth_certificate_filename else None
    )

    db.session.add(new_applicant)
    db.session.commit()

    return applicant_schema.jsonify(new_applicant), 201

# Route to get all applicants (Admin View)
@app.route('/applicants', methods=['GET'])
def get_applicants():
    applicants = Applicant.query.all()
    return applicants_schema.jsonify(applicants)

# Route to get a single applicant by ID
@app.route('/applicants/<int:id>', methods=['GET'])
def get_single_applicant(id):
    applicant = Applicant.query.get_or_404(id)
    return applicant_schema.jsonify(applicant)


@app.route('/applicants/<int:id>', methods=['PUT'])
def update_application_status(id):
    applicant = Applicant.query.get_or_404(id)  # Fetch applicant by ID or 404 if not found
    status = request.json.get('status')  # Get the new status from the request body

    # Ensure the status is either 'Approved' or 'Rejected'
    if status not in ['Approved', 'Rejected']:
        return jsonify({"error": "Invalid status. It must be 'Approved' or 'Rejected'."}), 400

    applicant.status = status  # Update the applicant's status

    try:
        db.session.commit()  # Commit the change to the database
        return applicant_schema.jsonify(applicant)  # Return the updated applicant data
    except Exception as e:
        db.session.rollback()  # Rollback in case of an error
        return jsonify({"error": str(e)}), 500  # Return an error message if something goes wrong


# Route to delete an applicant
@app.route('/applicants/<int:id>', methods=['DELETE'])
def delete_application(id):
    applicant = Applicant.query.get_or_404(id)
    db.session.delete(applicant)
    db.session.commit()

    return jsonify({"message": "Applicant deleted successfully"}), 200

# Route to update an applicant's details (e.g. when they need to make edits)
@app.route('/applicants/<int:id>/update', methods=['PUT'])
def update_applicant(id):
    applicant = Applicant.query.get_or_404(id)

    data = request.form
    errors = applicant_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    # Update the applicant details
    applicant.full_name = data['fullName']
    applicant.admission = data['admission']
    applicant.gender = data['gender']
    applicant.form = data['form']
    applicant.dob = data['dob']
    applicant.national_id = data['nationalID']
    applicant.phone_number = data['phoneNumber']
    applicant.email = data['email']
    applicant.institution_type = data['institutionType']
    applicant.institution_name = data['institutionName']
    applicant.index_number = data.get('indexNumber', '')
    applicant.constituency = data['constituency']
    applicant.ward = data['ward']

    # Handle file uploads if provided
    id_document_file = request.files.get('idDocument')
    birth_certificate_file = request.files.get('birthCertificate')

    if id_document_file and allowed_file(id_document_file.filename):
        id_document_filename = secure_filename(id_document_file.filename)
        id_document_file.save(os.path.join(app.config['UPLOAD_FOLDER'], id_document_filename))
        applicant.id_document = f'http://localhost:5000/uploads/{id_document_filename}'

    if birth_certificate_file and allowed_file(birth_certificate_file.filename):
        birth_certificate_filename = secure_filename(birth_certificate_file.filename)
        birth_certificate_file.save(os.path.join(app.config['UPLOAD_FOLDER'], birth_certificate_filename))
        applicant.birth_certificate = f'http://localhost:5000/uploads/{birth_certificate_filename}'

    db.session.commit()

    return applicant_schema.jsonify(applicant)

# the end of the bursary application functionality


# start of the key-achievements functionality
class AchievementSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Achievement
        load_instance = True

    id = ma.auto_field()
    title = ma.auto_field()
    description = ma.auto_field()
    img_url = ma.auto_field()
    icon = ma.auto_field()

achievement_schema = AchievementSchema()
achievements_schema = AchievementSchema(many=True)

@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/achievements', methods=['GET'])
def get_achievements():
    achievements = Achievement.query.all()
    return achievements_schema.jsonify(achievements)

@app.route('/achievements/<int:id>', methods=['GET'])
def get_achievement(id):
    achievement = Achievement.query.get_or_404(id)
    return achievement_schema.jsonify(achievement)

@app.route('/achievements', methods=['POST'])
def create_achievement():
    image = request.files.get('image')
    if not image or image.filename == '':
        return jsonify({"error": "No image file provided."}), 400
    if not allowed_file(image.filename):
        return jsonify({"error": "Invalid file type."}), 400

    # Ensure the upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    filename = secure_filename(image.filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(image_path)

    data = request.form
    title = data.get('title')
    description = data.get('description')
    if not title or not description:
        return jsonify({"error": "Title and description are required."}), 400

    new_achievement = Achievement(
        title=title,
        description=description,
        img_url=f'/images/{filename}',
        icon=data.get('icon')
    )
    db.session.add(new_achievement)
    db.session.commit()

    return achievement_schema.jsonify(new_achievement), 201

@app.route('/achievements/<int:id>', methods=['PUT'])
def update_achievement(id):
    achievement = Achievement.query.get_or_404(id)
    data = request.form

    title = data.get('title')
    description = data.get('description')
    if not title or not description:
        return jsonify({"error": "Title and description are required."}), 400

    image = request.files.get('image')
    if image and image.filename:
        if not allowed_file(image.filename):
            return jsonify({"error": "Invalid file type."}), 400

        # Ensure the upload directory exists
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)
        achievement.img_url = f'/images/{filename}'

    achievement.title = title
    achievement.description = description
    achievement.icon = data.get('icon')

    db.session.commit()
    return achievement_schema.jsonify(achievement)

@app.route('/achievements/<int:id>', methods=['DELETE'])
def delete_achievement(id):
    achievement = Achievement.query.get_or_404(id)
    db.session.delete(achievement)
    db.session.commit()
    return jsonify({"message": "Achievement deleted successfully"}), 200

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
# end of the key-achievement functionality


# start of the email functioninality
@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.json
    recipient = data['recipient']
    subject = data['subject']
    body = data['body']
    
    msg = Message(subject, recipients=[recipient])
    msg.body = body
    
    try:
        mail.send(msg)
        return jsonify({"message": "Email sent successfully"}), 200
    except Exception as e:
        return jsonify({"message": "Failed to send email", "error": str(e)}), 500





# -------------------- Main Function --------------------
if __name__ == '__main__':
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()  # Initialize database tables

    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)


