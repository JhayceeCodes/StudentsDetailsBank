from . import db
from flask_login import UserMixin
from sqlalchemy import Date
from datetime import datetime

class Student(db.Model,UserMixin):
    __tablename__ = "Students"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    matric_number = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    
    # One-to-one relationship with the 'Info' model
    info = db.relationship('Info', backref='student', uselist=False)

class Info(db.Model):
    __tablename__ = "students_information"
    id = db.Column(db.Integer, primary_key=True)
    university = db.Column(db.String(150), nullable=False)
    campus = db.Column(db.String(150), nullable=False)
    faculty = db.Column(db.String(150), nullable=False)
    department = db.Column(db.String(150), nullable=False)
    DOB = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(200), nullable=False)
    others = db.Column(db.String(1000), nullable=True)
    courses = db.Column(db.String(1000), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.now(), nullable=False)
    
    # Foreign key to 'Students' table
    student_id = db.Column(db.Integer, db.ForeignKey('Students.id'), unique=True, nullable=False)
