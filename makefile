# Makefile for converting Qt .ui files to Python files using pyuic6

# Directory containing .ui files
UI_DIR = qt_creator_files

# Output directory for generated .py files
OUTPUT_DIR = src/view

# Find all .ui files in the UI_DIR
UI_FILES = $(wildcard $(UI_DIR)/*.ui)

# Generate corresponding .py file names in the output directory
PY_FILES = $(patsubst $(UI_DIR)/%.ui,$(OUTPUT_DIR)/%.py,$(UI_FILES))

# Default target - convert all .ui files to .py files
uic: $(PY_FILES)

# Rule to convert .ui files to .py files
$(OUTPUT_DIR)/%.py: $(UI_DIR)/%.ui
	@if not exist "$(OUTPUT_DIR)" mkdir "$(OUTPUT_DIR)"
	pyuic6 $< -o $@

# Clean target to remove generated .py files
clean:
	powershell -Command "Remove-Item -Path '$(OUTPUT_DIR)\Ui_*.py' -Force -ErrorAction SilentlyContinue"

# Force rebuild all files
rebuild: clean uic

# Show what files will be processed
show-files:
	@echo "UI files found:"
	@echo "$(UI_FILES)"
	@echo "Will generate:"
	@echo "$(PY_FILES)"