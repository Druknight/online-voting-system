ONLINE VOTING DEMO — OPEN LINK, ADMIN-ONLY RESULTS

CANDIDATES
1. Angeline
2. Sifuna
3. Lenah
4. Fidel

HOW IT WORKS
- Anyone with the website link can open the voting page.
- A voter selects one candidate and submits.
- Results are only visible at /results after the administrator password is entered.
- The app blocks a second vote from the same browser cookie.

IMPORTANT LIMITATION
Open-link voting cannot reliably prove that each human votes only once. This demo uses a browser cookie to discourage repeat voting; people can bypass it by switching browsers/devices or clearing cookies. Do not use this for official, high-stakes, or legally binding elections. For stronger controls, use unique voter codes or verified accounts.

LOCAL TESTING (Windows PowerShell)
1. Install Python 3.10+.
2. In this folder run: pip install -r requirements.txt
3. Set:
   $env:SECRET_KEY="replace-with-a-long-random-secret"
   $env:ADMIN_PASSWORD="replace-with-a-strong-admin-password"
4. Start: python app.py
5. Open http://127.0.0.1:5000
6. Admin results: http://127.0.0.1:5000/results

PUBLISHING WITH RENDER
1. Create a GitHub account if needed.
2. Create a new GitHub repository and upload every file and folder in this package.
3. In Render, choose New + > Web Service and connect the GitHub repository.
4. Choose Python. Build command: pip install -r requirements.txt
   Start command: gunicorn app:app
5. In Render Environment, add SECRET_KEY (a long random secret) and ADMIN_PASSWORD (a strong unique password). Keep both private.
6. Deploy. Render provides a public HTTPS link to share with voters.
7. Admin opens https://YOUR-SITE/results and enters the admin password.

DATABASE / HOSTING WARNING
This starter uses SQLite in a local file. Some hosting plans use temporary filesystems or may replace files during deploy/restart. Before relying on votes, configure persistent storage or use a managed PostgreSQL database and test backups/restarts. Check the host's current storage rules.

This is a classroom/demo tool, not a certified election platform.
