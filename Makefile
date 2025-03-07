# Define the virtual environment directory
VENV_DIR = .venv

# Create and activate virtual environment
create_venv:
	python -m venv $(VENV_DIR)
	@echo "Virtual environment created."

# Install dependencies from requirements.txt
install_requirements: create_venv
	$(VENV_DIR)/Scripts/pip install -r requirements.txt
	@echo "Dependencies installed."

# Run the server
run_server:
	$(VENV_DIR)/Scripts/python src/server.py

# Run the client
run_client:
	$(VENV_DIR)/Scripts/python src/client.py

# Clean the virtual environment
clean:
	rm -rf $(VENV_DIR)
	@echo "Cleaned the virtual environment."
