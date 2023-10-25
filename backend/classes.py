from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum

db = SQLAlchemy()

class Role(db.Model):
    __tablename__ = 'ROLE_DETAILS'

    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), nullable=False)
    role_description = db.Column(db.String(50000), nullable=False)
    role_status = db.Column(Enum('active', 'inactive'), nullable=False)
    role_skills = db.relationship('Role_skill', backref='role')

    def __init__(self, role_id, role_name, role_description, role_status):
        self.role_id = role_id
        self.role_name = role_name
        self.role_description = role_description
        self.role_status = role_status

    def json(self):
        return {"role_id": self.role_id, "role_name": self.role_name, "role_description": self.role_description, "role_status": self.role_status}

class Role_listing(db.Model):
    __tablename__ = 'ROLE_LISTINGS'

    role_listing_id = db.Column(db.Integer, primary_key=True, unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('ROLE_DETAILS.role_id'))
    role_listing_desc = db.Column(db.String(5000))
    role_listing_source = db.Column(db.Integer, db.ForeignKey('STAFF_DETAILS.staff_id'))
    role_listing_open = db.Column(db.Date)
    role_listing_close = db.Column(db.Date, nullable=True)
    role_listing_creator = db.Column(db.Integer, db.ForeignKey('STAFF_DETAILS.staff_id'))
    role_listing_ts_create = db.Column(db.Date)
    role_listing_updater = db.Column(db.Integer, db.ForeignKey('STAFF_DETAILS.staff_id'))
    role_listing_ts_update = db.Column(db.Date)

    role = db.relationship('Role', foreign_keys=[role_id])
    source_staff = db.relationship('Staff', foreign_keys=[role_listing_source])
    creator_staff = db.relationship('Staff', foreign_keys=[role_listing_creator])
    updater_staff = db.relationship('Staff', foreign_keys=[role_listing_updater])

    def __init__(self, role_listing_id, role_id, role_listing_desc, role_listing_source, role_listing_open, role_listing_close, role_listing_creator, role_listing_ts_create, role_listing_updater, role_listing_ts_update):
        self.role_listing_id = role_listing_id
        self.role_id = role_id
        self.role_listing_desc = role_listing_desc
        self.role_listing_source = role_listing_source
        self.role_listing_open = role_listing_open
        self.role_listing_close = role_listing_close
        self.role_listing_creator = role_listing_creator
        self.role_listing_ts_create = role_listing_ts_create
        self.role_listing_updater = role_listing_updater
        self.role_listing_ts_update = role_listing_ts_update
    
    def json(self):
        return {
            "role_listing_id": self.role_listing_id,
            "role_id": self.role_id,
            "role_listing_desc": self.role_listing_desc,
            "role_listing_source": self.role_listing_source,
            "role_listing_open": self.role_listing_open,
            "role_listing_close": self.role_listing_close,
            "role_listing_creator": self.role_listing_creator,
            "role_listing_ts_create": self.role_listing_ts_create,
            "role_listing_updater": self.role_listing_updater,
            "role_listing_ts_update": self.role_listing_ts_update,
        }

class Role_application(db.Model):
    __tablename__ = 'ROLE_APPLICATIONS'

    role_app_id = db.Column(db.Integer, primary_key=True)
    role_listing_id = db.Column(db.Integer, db.ForeignKey('ROLE_LISTINGS.role_listing_id', ondelete='CASCADE'))
    staff_id = db.Column(db.Integer, db.ForeignKey('STAFF_DETAILS.staff_id', ondelete='CASCADE'))
    role_app_status = db.Column(Enum('applied', 'withdrawn'), nullable=False)
    role_app_ts_create = db.Column(db.Date)

    role_listing = db.relationship('Role_listing', backref='applications', foreign_keys=[role_listing_id])
    staff = db.relationship('Staff', backref='applications', foreign_keys=[staff_id])

    def __init__(self, role_app_id, role_listing_id, staff_id, role_app_status, role_app_ts_create, role_listing, staff):
        self.role_app_id = role_app_id
        self.role_listing_id = role_listing_id
        self.staff_id = staff_id
        self.role_app_status = role_app_status
        self.role_app_ts_create = role_app_ts_create
        self.role_listing = role_listing
        self.staff = staff
    
    def json(self):
        return {
            "role_app_id": self.role_app_id,
            "role_listing_id": self.role_listing_id,
            "staff_id": self.staff_id,
            "role_app_status": self.role_app_status,
            "role_app_ts_create": self.role_app_ts_create,
            "role_listing": self.role_listing,
            "staff": self.staff
        }

class Role_skill(db.Model):
    __tablename__ = 'ROLE_SKILLS'

    role_id = db.Column(db.Integer, db.ForeignKey('ROLE_DETAILS.role_id', ondelete='CASCADE'), primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('SKILL_DETAILS.skill_id', ondelete='CASCADE'), primary_key=True)

    def __init__(self, role_id, skill_id):
        self.role_id = role_id
        self.skill_id = skill_id

    def json(self):
        return {
            "role_id": self.role_id,
            "skill_id": self.skill_id
        }

class Skill(db.Model):
    __tablename__ = 'SKILL_DETAILS'

    skill_id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(50), nullable=False)
    skill_status = db.Column(Enum('active', 'inactive'), nullable=False)
    role_skills = db.relationship('Role_skill', backref='skill')
    

    def __init__(self, skill_id, skill_name, skill_status):
        self.skill_id = skill_id
        self.skill_name = skill_name
        self.skill_status = skill_status

    def json(self):
        return {"skill_id": self.skill_id, "skill_name": self.skill_name, "skill_status": self.skill_status}

class Staff(db.Model):
    __tablename__ = 'STAFF_DETAILS'

    staff_id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50), nullable = False)
    lname = db.Column(db.String(50), nullable=False)
    dept = db.Column(db.Integer)
    email = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    biz_address = db.Column(db.String(255))
    sys_role = db.Column(db.String(15))

    def __init__(self, staff_id, fname, lname, dept, email, phone, biz_address, sys_role):
        self.staff_id = staff_id
        self.fname = fname
        self.lname = lname
        self.dept = dept
        self.email = email
        self.phone = phone
        self.biz_address = biz_address
        self.sys_role = sys_role

    def json(self):
        return {"staff_id": self.staff_id, "fname": self.fname, "lname":self.lname, "dept": self.dept, "email": self.email, "phone": self.phone, "biz_address": self.biz_address, "sys_role": self.sys_role}

class RO(db.Model):
    __tablename__ = 'STAFF_REPORTING_OFFICER'

    staff_id = db.Column(db.Integer, primary_key=True)
    RO_id = db.Column(db.Integer)

    def __init__(self, staff_id, RO_id):
        self.staff_id = staff_id
        self.RO_id = RO_id

    def json(self):
        return {"staff_id": self.staff_id, "RO_id": self.RO_id}

class Staff_roles(db.Model):
    __tablename__ = 'STAFF_ROLES'

    staff_id = db.Column(db.Integer, primary_key=True)
    staff_role = db.Column(db.Integer, primary_key=True)
    role_type = db.Column(db.String(9))
    sr_status = db.Column(db.String(8))

    def __init__(self, staff_id, staff_role, role_type, sr_status):
        self.staff_id = staff_id
        self.staff_role = staff_role
        self.role_type = role_type
        self.sr_status = sr_status
    
    def json(self):
        return {"staff_id": self.staff_id, "staff_role":self.staff_role, "role_type":self.role_type, "sr_status":self.sr_status}

class Skills(db.Model):
    __tablename__ = 'STAFF_SKILLS'

    staff_id = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.Integer, primary_key=True)
    ss_status = db.Column(db.String(8))

    def __init__(self, staff_id, skill_id, ss_status):
        self.staff_id = staff_id
        self.skill_id = skill_id
        self.ss_status = ss_status

    def json(self):
        return {"staff_id":self.staff_id, "skill_id": self.skill_id, "ss_status": self.ss_status}