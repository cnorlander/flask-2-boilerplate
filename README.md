# Flask Boilerplate
## Work in progress!

This is a basic Flask web application created to be a jumping off point for future apps. Some features will include:
- [X] Auth w/ Flask Logon and Bcrypt.
- [X] Password Reset Feature.
- [X] Flask-SQLAlchemy for ORM.
- [X] SQLite DB file for portability
- [X] A Fancy logon page.
- [X] A menu template
- [ ] Some basic page templates.
- [ ] A user management page.
- [ ] A role management page.
- [X] An easy to use and flexible role and action system for managing permissions
- [X] Docker and Docker-Compose files for easy deployment
- [X] Gunicorn WSGI HTTP Server
- [X] NGINX for reverse proxy and serving static files
- [X] Automatic Self-Signed SSL Generation

While this project has some good bones if you decide to build your app on this you may want to do the following:
- Integrate SSO with Python-SAML or OpenID
- Swap out SQLite for a proper database such as MySQL or Postgress or go NoSQL
- Switch to UUIDs for Primary Keys
