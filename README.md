# E-voting-App

**Refactored application Structure**
e_voting_system/
│
├── main.py
├── app.py
│
├── models/
│   ├── __init__.py
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
│   ├── __init__.py
│   └── data_repository.py
│
├── services/
│   ├── __init__.py
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
│   ├── __init__.py
│   ├── console_ui.py
│   ├── login_ui.py
│   ├── admin_ui.py
│   └── voter_ui.py
│
├── utils/
│   ├── __init__.py
│   ├── constants.py
│   ├── helpers.py
│   ├── validators.py
│   └── security.py
│
└── data/
    └── evoting_data.json

-----------

