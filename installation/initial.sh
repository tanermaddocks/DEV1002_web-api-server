# Initialise virtual environment
rm -r .venv
python3 -m venv .venv
source .venv/bin/activate
echo "Virtual environemt installed and activated"
# Install dependencies
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt
pip3 freeze > requirements.txt
echo "Dependencies installed"
# Create .env file
rm .env
touch .env
echo 'DATABASE_URI="postgresql+psycopg2://DATABASE_OWNER:PASSWORD@localhost:5432/DATABASE_NAME"' > .env
echo "Flask environment file created and URI format added for local environments"
# Print further instructions
echo ""
echo "For local installs use postgreSQL to create a database and then input the DATABASE_URI in the .env file"
echo "Use this format, replacing DATABASE_OWNER, PASSWORD and DATABASE_NAME for a local environment: "
echo 'DATABASE_URI="postgresql+psycopg2://DATABASE_OWNER:PASSWORD@localhost:5432/DATABASE_NAME"'