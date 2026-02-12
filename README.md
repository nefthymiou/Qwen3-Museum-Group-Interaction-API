Qwen3-Museum-Group-Interaction-API

This project uses a Vision-Language Model (LVLM) to analyze group behavior in museum settings. It extracts demographic data, spatial formations, and engagement levels from images or video frames using a highly constrained system prompt.

Features
- Vision-AI Analysis: Uses Qwen-series models to interpret complex human group dynamics.
- Strict JSON Output: Returns structured data ready for database insertion or real-time dashboards.
- Flask API: A lightweight REST interface to send images and receive behavior metrics.


### Installation

conda env create -f environment.yml
conda activate qwen3-api
conda install OpenCV

### Install Ollama (if not already installed)
curl -fsSL https://ollama.com/install.sh | sh

### Pull the needed Qwen model 
ollama pull qwen3-vl:8b
ollama pull qwen3-vl:2b

Run the API

### Running the API Server
python app.py

### Testing the video
python test_video.py

