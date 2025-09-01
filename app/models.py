from sqlalchemy import Column, Integer, String, Text, Enum
from app.db import Base
import enum

# Admin Table
class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(200), nullable=False)  # hashed password

# Hero Section
class Hero(Base):
    __tablename__ = "hero"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(500))
    resume_file = Column(String(255))  # store filename/path
    image_file = Column(String(255))   # store filename/path


class About(Base):
    __tablename__ = "about"

    id = Column(Integer, primary_key=True, index=True)
    des1 = Column(String(500))
    des2 = Column(String(500))



class SkillStatus(enum.Enum):
    active = "a"
    inactive = "i"
    deleted = "d"


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    image_file = Column(String(255), nullable=True)
    status = Column(Enum(SkillStatus), default=SkillStatus.active, nullable=False)

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    image_file = Column(String(255), nullable=True)
    project_url = Column(String(255), nullable=True)
    status = Column(Enum(SkillStatus), default=SkillStatus.active, nullable=False)


class Education(Base):
    __tablename__ = "education"

    id = Column(Integer, primary_key=True, index=True)
    heading = Column(String(255), nullable=False)
    institute_string = Column(String(255))
    des_string = Column(String(500))
    score_string = Column(String(100))
    institute_link = Column(String(255))
    year_string = Column(String(50))
    status = Column(Enum(SkillStatus), default=SkillStatus.active, nullable=False)



class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), nullable=False)
    value = Column(String(255), nullable=False)
    status = Column(Enum(SkillStatus), default=SkillStatus.active, nullable=False)

    
# # Education Section
# class Education(Base):
#     __tablename__ = "education"
#     id = Column(Integer, primary_key=True, index=True)
#     degree = Column(String(200), nullable=False)
#     institution = Column(String(200), nullable=False)
#     year = Column(String(50))

# # Experience Section
# class Experience(Base):
#     __tablename__ = "experience"
#     id = Column(Integer, primary_key=True, index=True)
#     role = Column(String(200), nullable=False)
#     company = Column(String(200), nullable=False)
#     duration = Column(String(100))
#     description = Column(Text)

# # Skills Section
# class Skills(Base):
#     __tablename__ = "skills"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(100), nullable=False)
#     level = Column(String(100))  # e.g. Beginner, Intermediate, Expert

# # Contact Section
# class Contact(Base):
#     __tablename__ = "contact"
#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String(200), nullable=False)
#     phone = Column(String(50))
#     address = Column(String(255))
#     linkedin = Column(String(255))
#     github = Column(String(255))
