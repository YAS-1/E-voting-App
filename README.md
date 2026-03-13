# E-voting-App

# 


# E-Voting Console Application (Refactored)

## 1. Project Overview

This project is a console-based electronic voting system developed in
Python. The system allows administrators to manage elections and voters
to participate in secure voting processes.

The application supports: - Voter registration - Voter verification -
Candidate management - Poll creation - Voting - Result tallying -
Reporting and statistics - Audit logging

The system was originally implemented as a single large monolithic
Python script. This project refactors the system to follow Software
Construction principles, improving:

-   Modularity
-   Maintainability
-   Readability
-   Separation of concerns
-   Object-oriented design

Importantly, the behavior and flow of the system remain identical to the
original application.

------------------------------------------------------------------------

## 2. Original System Problems

### 2.1 Monolithic Design

All functionality was contained in one file, including: - UI logic -
Business logic - Data storage - Authentication - Voting logic - Result
computation

This made the system difficult to maintain and extend.

### 2.2 Global State

The original system relied heavily on global variables such as: -
voters - candidates - voting_stations - polls - votes - audit_log -
current_user - current_role

This tightly coupled different parts of the system and made debugging
difficult.

### 2.3 Mixed Responsibilities

Many functions handled multiple responsibilities simultaneously. For
example, the poll results function performed vote counting, aggregation,
statistics calculation, formatting, and printing UI output.

This violated the Single Responsibility Principle (SRP).

### 2.4 Poor Modularity

The system lacked clear separation between: - UI - Business logic - Data
storage - Domain models

This made testing and maintenance difficult.

------------------------------------------------------------------------

## 3. Refactoring Goals

The refactoring aimed to: 1. Maintain the exact same application
behavior 2. Improve code organization 3. Apply Object Oriented Design 4.
Apply Software Construction best practices 5. Apply SOLID principles
where appropriate

------------------------------------------------------------------------

## 4. Refactored Architecture

User Interface (UI Layer) ↓ Service Layer (Business Logic) ↓ Repository
Layer (Data Access) ↓ Models + Utilities

Each layer has a clear responsibility.

------------------------------------------------------------------------

## 5. Project Structure

**Refactored application Structure**
e_voting_system/
│
├── main.py
├── app.py
│
├── models/
│   ├── admin.py
│   ├── voter.py
│   ├── candidate.py
│   ├── voting_station.py
│   ├── position.py
│   ├── poll.py
│   ├── vote.py
│   └── audit_entry.py
│
├── repositories/
│   └── data_repository.py
│
├── services/
│   ├── auth_service.py
│   ├── admin_service.py
│   ├── voter_service.py
│   ├── candidate_service.py
│   ├── station_service.py
│   ├── position_service.py
│   ├── poll_service.py
│   ├── voting_service.py
│   ├── results_service.py
│   └── audit_service.py
│
├── ui/
│   ├── console_ui.py
│   ├── login_ui.py
│   ├── admin_ui.py
│   └── voter_ui.py
│
├── utils/
│   ├── constants.py
│   ├── helpers.py
│   ├── validators.py
│   └── security.py
│
└── data/
    └── evoting_data.json


------------------------------------------------------------------------

## 6. Layer Responsibilities

### UI Layer

Handles all user interaction.

Responsibilities: - Display menus - Collect user input - Show results

UI classes do not contain business logic.

### Service Layer

The core business logic is implemented in services such as: -
VoterService - CandidateService - PollService - VotingService -
ResultsService - AdminService

These services handle the operations and rules of the system.

### Repository Layer

The DataRepository manages data persistence.

Responsibilities: - Load system data from JSON - Store system data -
Provide centralized access to data

This replaces the original global variables.

### Model Layer

Models represent the core domain objects: - Voter - Candidate - Poll -
Position - Admin - VotingStation

These represent structured data used across the system.

------------------------------------------------------------------------

## 7. Software Construction Principles Applied

### Separation of Concerns

The system separates UI, business logic, and data access into different
layers.

### Single Responsibility Principle

Each class performs a single well-defined task.

### Encapsulation

Data is handled through classes and services rather than global
variables.

### Modularity

The system is divided into logical modules, improving maintainability.

### Maintainability

The refactored code is easier to understand, modify, and extend.

------------------------------------------------------------------------

## 8. Features of the System

### Voter Features

-   Voter registration
-   Voter login
-   View open polls
-   Cast vote
-   Abstain from positions
-   View voting history
-   View poll results
-   Change password
-   View personal profile

### Admin Features

Candidate Management - Create candidate - Update candidate - Search
candidates - Deactivate candidate

Station Management - Create station - Update station - Deactivate
station

Poll Management - Create poll - Assign candidates - Open/close poll -
Delete poll

Voter Management - View voters - Verify voters - Deactivate voters -
Search voters

Admin Management - Create admin - View admins - Deactivate admins

### Reporting Features

-   Poll results
-   Station-wise results
-   Detailed statistics
-   Audit log

------------------------------------------------------------------------

## 9. Security Features

The system includes: - Password hashing - Voter verification -
Role-based admin permissions - Audit logging of system actions -
Prevention of duplicate voting

------------------------------------------------------------------------

## 10. Running the System

### Requirements

Python 3.9+

### Run the Application

python main.py

------------------------------------------------------------------------

## 11. Data Persistence

System data is stored in:

data/system_data.json

The repository automatically loads data at startup and saves it when
changes occur.

------------------------------------------------------------------------

## 12. Refactoring Outcome

The refactoring transformed the original monolithic script into a
modular, maintainable, object-oriented system while preserving the
original behavior and workflow.

Key improvements: - Cleaner architecture - Improved readability - Easier
debugging - Better separation of concerns - Stronger adherence to
Software Construction principles

