# from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from flask_marshmallow import Marshmallow
# from flask_cors import CORS

# # Initialize Flask app
# app = Flask(__name__)
# CORS(app)

# # Database configuration
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///adminaction.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# CORS(app, resources={r"/applicants": {"origins": "http://localhost:3000"}})


# db = SQLAlchemy(app)
# ma = Marshmallow(app)

# # Database Model
# class Applicant(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     full_name = db.Column(db.String(100), nullable=False)
#     admission = db.Column(db.String(50), nullable=False)
#     gender = db.Column(db.String(10), nullable=False)
#     institution_name = db.Column(db.String(100), nullable=False)
#     national_id = db.Column(db.String(20), nullable=False)
#     email = db.Column(db.String(100), nullable=False)
#     constituency = db.Column(db.String(100), nullable=False)
#     ward = db.Column(db.String(100), nullable=False)
#     id_document = db.Column(db.String(200), nullable=True)
#     birth_certificate = db.Column(db.String(200), nullable=True)
#     status = db.Column(db.String(20), default='Pending')

# # Marshmallow Schema
# class ApplicantSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Applicant
#         include_fk = True

# applicant_schema = ApplicantSchema()
# applicants_schema = ApplicantSchema(many=True)

# # Routes

# # Fetch all applicants
# @app.route('/applicants', methods=['GET'])
# def get_applicants():
#     applicants = Applicant.query.all()
#     return applicants_schema.jsonify(applicants)

# # Update applicant status
# @app.route('/applicants/<int:applicant_id>', methods=['PATCH'])
# def update_applicant_status(applicant_id):
#     applicant = Applicant.query.get(applicant_id)
#     if not applicant:
#         return jsonify({"error": "Applicant not found"}), 404

#     data = request.get_json()
#     status = data.get('status')

#     if status not in ['Approved', 'Rejected', 'Pending']:
#         return jsonify({"error": "Invalid status"}), 400

#     applicant.status = status
#     db.session.commit()
#     return applicant_schema.jsonify(applicant)

# # Create database and sample data (Run only once)
# @app.cli.command('initdb')
# def initdb():
#     db.create_all()
#     # Add sample applicants
#     sample_applicants = [
#         Applicant(
#             full_name='John Doe',
#             admission='ADM001',
#             gender='Male',
#             institution_name='Example University',
#             national_id='12345678',
#             email='johndoe@example.com',
#             constituency='Nairobi',
#             ward='Westlands',
#             id_document='/path/to/id1.jpg',
#             birth_certificate='/path/to/birth1.jpg'
#         ),
#         Applicant(
#             full_name='Jane Smith',
#             admission='ADM002',
#             gender='Female',
#             institution_name='Sample College',
#             national_id='87654321',
#             email='janesmith@example.com',
#             constituency='Mombasa',
#             ward='Nyali',
#             id_document='/path/to/id2.jpg',
#             birth_certificate='/path/to/birth2.jpg'
#         )
#     ]
#     db.session.bulk_save_objects(sample_applicants)
#     db.session.commit()
#     print('Database initialized with sample data!')

# # Run the Flask app
# if __name__ == '__main__':
#     app.run(debug=True)




from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Database configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, 'adminaction.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

# Database Model
class Applicant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    admission = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    institution_name = db.Column(db.String(100), nullable=False)
    national_id = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    constituency = db.Column(db.String(100), nullable=False)
    ward = db.Column(db.String(100), nullable=False)
    id_document = db.Column(db.String(200), nullable=True)
    birth_certificate = db.Column(db.String(200), nullable=True)
    status = db.Column(db.String(20), default='Pending')

# Marshmallow Schema
class ApplicantSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Applicant
        include_fk = True

applicant_schema = ApplicantSchema()
applicants_schema = ApplicantSchema(many=True)

# Routes


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
# # Fetch all applicants
# @app.route('/applicants', methods=['GET'])
# def get_applicants():
#     try:
#         applicants = Applicant.query.all()
#         return applicants_schema.jsonify(applicants), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# Update applicant status
@app.route('/applicants/<int:applicant_id>', methods=['PATCH'])
def update_applicant_status(applicant_id):
    try:
        applicant = Applicant.query.get(applicant_id)
        if not applicant:
            return jsonify({"error": "Applicant not found"}), 404

        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400

        status = data.get('status')
        if status not in ['Approved', 'Rejected', 'Pending']:
            return jsonify({"error": "Invalid status"}), 400

        applicant.status = status
        db.session.commit()
        return applicant_schema.jsonify(applicant), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Create database and sample data (Run only once)
@app.cli.command('initdb')
def initdb():
    try:
        db.create_all()
        # Add sample applicants only if table is empty
        if not Applicant.query.first():
            sample_applicants = [
                Applicant(
                    full_name='John Doe',
                    admission='ADM001',
                    gender='Male',
                    institution_name='Example University',
                    national_id='12345678',
                    email='johndoe@example.com',
                    constituency='Nairobi',
                    ward='Westlands',
                    id_document='/path/to/id1.jpg',
                    birth_certificate='/path/to/birth1.jpg'
                ),
                Applicant(
                    full_name='Jane Smith',
                    admission='ADM002',
                    gender='Female',
                    institution_name='Sample College',
                    national_id='87654321',
                    email='janesmith@example.com',
                    constituency='Mombasa',
                    ward='Nyali',
                    id_document='/path/to/id2.jpg',
                    birth_certificate='/path/to/birth2.jpg'
                )
            ]
            db.session.bulk_save_objects(sample_applicants)
            db.session.commit()
            print('Database initialized with sample data!')
        else:
            print('Database already initialized.')
    except Exception as e:
        print(f"Error initializing the database: {e}")

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
