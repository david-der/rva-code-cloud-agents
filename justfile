# List available commands
default:
    @just --list

# Install all dependencies
install:
    poetry install

# Update all dependencies
update:
    poetry update

# Generate text using OpenAI (optional prompt)
text-gen *PROMPT="Tell me an interesting fact about Richmond, Virginia":
    set dotenv-load
    poetry run python -m rva_code_cloud_agents.main text "{{PROMPT}}"

# Generate image using OpenAI (optional prompt)
image-gen *PROMPT="A beautiful sunset over Richmond, Virginia skyline with the James River in the foreground":
    set dotenv-load
    poetry run python -m rva_code_cloud_agents.main image "{{PROMPT}}"

# Generate standard PowerPoint
pptx-gen *PROMPT="A modern tech background with abstract digital elements":
    set dotenv-load
    poetry run python -m rva_code_cloud_agents.main pptx "{{PROMPT}}"

# Generate analytics presentation
pptx-analytics *CHARTS="charts/*.png":
    set dotenv-load
    poetry run python -m rva_code_cloud_agents.main pptx-analytics "An industrial cityscape with data visualization elements" "{{CHARTS}}"