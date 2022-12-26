set -e
set FLASK_APP=core/server.py

flask db init -d core/migrations/
flask db migrate -m "Initial migration." -d core/migrations/
flask db upgrade -d core/migrations/

