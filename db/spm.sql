CREATE DATABASE IF NOT EXISTS LMS DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE LMS;

DROP TABLE IF EXISTS STAFF_DETAILS;
CREATE TABLE STAFF_DETAILS (
    staff_id int NOT NULL UNIQUE,
    fname varchar(50) NOT NULL,
    lname varchar(50) NOT NULL,
    dept varchar(50) NOT NULL,
    email varchar(50) NOT NULL,
    phone varchar(20) NOT NULL,
    biz_address varchar(255) NOT NULL,
    sys_role ENUM('staff', 'hr', 'manager', 'inactive'),
    PRIMARY KEY (staff_id)
);

INSERT INTO STAFF_DETAILS VALUES
(123456789, 'AH GAO', 'TAN', 'FINANCE', 'tan_ah_gao@all-in-one.com.sg', '65-1234-5678', 'address1', 'staff'),
(123456788, 'VINCENT REX', 'COLINS', 'HUMAN RESOURCE AND ADMIN', 'colins_email@email.com.sg', '65-1234-5679', 'address2','hr'),
(123456787, 'FAUD', 'NIZAM', 'SALES', 'faud_email@email.com.sg', '60-1234-5678', 'address3', 'manager'),
(123456786, 'JOHN', 'DOE', 'IT', 'john_email@email.com.sg', '69-6969696969', 'address4', 'inactive'),
(1, 'BOSS', 'PERSON', 'HEAD OFFICE', 'boss@email.com.sg', '42-0420-4204', 'bossaddress', 'manager');

DROP TABLE IF EXISTS STAFF_REPORTING_OFFICER;
CREATE TABLE STAFF_REPORTING_OFFICER (
    staff_id int NOT NULL,
    RO_id int NULL,
    PRIMARY KEY (staff_id),
    FOREIGN KEY (staff_id) 
    REFERENCES STAFF_DETAILS(staff_id) 
    ON DELETE CASCADE 
    ON UPDATE CASCADE,
    FOREIGN KEY (RO_id) 
    REFERENCES STAFF_DETAILS(staff_id) 
    ON DELETE SET NULL
);

INSERT INTO STAFF_REPORTING_OFFICER VALUES
(123456789, 123456787),
(123456788, 1);

CREATE DATABASE IF NOT EXISTS LJPS DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE LJPS;

DROP TABLE IF EXISTS ROLE_DETAILS;
CREATE TABLE ROLE_DETAILS (
    role_id int NOT NULL,
    role_name varchar(50) NOT NULL,
    role_description varchar(50000) NOT NULL,
    role_status ENUM('active', 'inactive'),
    PRIMARY KEY (role_id)
);

INSERT INTO ROLE_DETAILS VALUES
(234567891, 'Head, Talent Attraction', "The Head, Talent Attraction is responsible for strategic workforce planning to support the organisation's growth strategies through establishing talent sourcing strategies, determining the philosophy for the selection and securing of candidates and overseeing the onboarding and integration of new hires into the organisation. He/She develops various approaches to meet workforce requirements and designs employer branding strategies. He oversees the selection processes and collaborates with business stakeholders for the hiring of key leadership roles. As a department head, he is responsible for setting the direction and articulating goals and objectives for the team, and driving the integration of Skills Frameworks across the organisation's talent attraction plans.

The Head, Talent Attraction is an influential and inspiring leader who adopts a broad perspective in the decisions he makes. He is articulate and displays a genuine passion for motivating and developing his team.", 'inactive'
),
(234567892, 'Learning Facilitator/ Trainer', "The Learning Facilitator delivers learning products and services in a variety of environments, using multiple learning delivery modes and methods. He/She assesses learning needs and adapts the facilitation approach to reflect desired learning outcomes and learner needs. He is responsible for knowledge and skills transfer by delivering learning content, facilitating group discussions and responding to queries. He drives learner development and commitment to continuous learning by actively providing feedback and learner support. He evaluates curriculum effectiveness and recommends improvement areas by collecting learner feedback as well as analysing learning delivery approaches and materials. 

He is a strong communicator who builds trusted relationships and creates a cooperative and engaging learning environment. He is adaptable and adept at managing multiple stakeholders. 

He works in multiple different environments, including different learning venues and client sites, and regularly interacts with digital systems.",
'active'),
(234567893, 'Agile Coach (SM)', "The Agile Coach (SM) coaches teams in the conduct of Agile practices and the implementation of Agile methodologies and practices in the organisation and acts as an effective Scrum Master in Agile Scrum teams.", 'active'),
(234567894, 'Fire Warden', "The Fire Warden is responsible for testing fire alarms and firefighting equipment and implementing risk assessment recommendations. In the event of a confirmed fire alarm or fire drill, the warden assists in the safe evacuation of staff and visitors from the premise immediately.", 'active');

DROP TABLE IF EXISTS STAFF_ROLES;
CREATE TABLE STAFF_ROLES (
    staff_id int NOT NULL,
    staff_role int NOT NULL,
    role_type ENUM('primary', 'secondary'),
    sr_status ENUM('active', 'inactive'),
    PRIMARY KEY (staff_id, staff_role),
    FOREIGN KEY (staff_role) REFERENCES ROLE_DETAILS(role_id)
    ON DELETE CASCADE
);

INSERT INTO STAFF_ROLES VALUES 
(123456789, 234567891, 'primary', 'active'),
(123456789, 234567892, 'secondary', 'active'),
(123456789, 234567893, 'secondary', 'inactive');

DROP TABLE IF EXISTS SKILL_DETAILS;
CREATE TABLE SKILL_DETAILS (
    skill_id int NOT NULL,
    skill_name varchar(50) NOT NULL,
    skill_status ENUM('active', 'inactive'),
    PRIMARY KEY (skill_id)
);

INSERT INTO SKILL_DETAILS VALUES 
(345678912, 'Pascal Programming', 'inactive'),
(345678913, 'Python Programming', 'active'),
(345678914, 'Certified Scrum Master', 'active'),
(345678969, 'Certified Freak', 'inactive'),
(345678970, 'Java Programming', 'active'),
(345678971, 'Certified Water Hose', 'active');

DROP TABLE IF EXISTS STAFF_SKILLS;
CREATE TABLE STAFF_SKILLS (
    staff_id int NOT NULL,
    skill_id int NOT NULL,
    ss_status ENUM('active', 'inactive', 'unverified', 'in-progress'),
    FOREIGN KEY (skill_id) REFERENCES SKILL_DETAILS(skill_id) ON DELETE CASCADE,
    PRIMARY KEY (staff_id, skill_id)
);

INSERT INTO STAFF_SKILLS VALUES
(123456789, 345678913, 'active'),
(123456789, 345678914, 'active'),
(123456789, 345678969, 'inactive'),
(123456789, 345678970, 'in-progress');

DROP TABLE IF EXISTS ROLE_SKILLS;
CREATE TABLE ROLE_SKILLS (
    role_id int NOT NULL,
    skill_id int NOT NULL,
    PRIMARY KEY (role_id, skill_id),
    FOREIGN KEY (role_id) REFERENCES ROLE_DETAILS(role_id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES SKILL_DETAILS(skill_id) ON DELETE CASCADE
);

INSERT INTO ROLE_SKILLS VALUES
(234567893, 345678914),
(234567891, 345678970),
(234567894, 345678971);