# RDDL-Code-Generator

## Project Overview
This project automates the translation of natural language descriptions into RDDL (Relational Dynamic Influence Diagram Language) code, creating environments for decision-making and planning simulations. The generated RDDL code is designed to work within the pyRDDLGym environment, making it suitable for reinforcement learning applications.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Demo Video](#project-demo-video)
- [Installation](#installation)
- [Usage](#usage)
- [Data](#data)
- [Project Structure](#project-structure)
- [License](#license)

## Features
- Automates the generation of RDDL code from natural language descriptions.
- Supports iterative error feedback to improve code quality until it’s compilable.
- Integrates with pyRDDLGym to enable reinforcement learning simulations.
- Utilizes Nvidia and OpenAI APIs for embedding and text generation.

## Project Demo Video
Watch a short video explaining this project:

[![Watch the video](https://img.youtube.com/vi/WW8_69AsBcM/0.jpg)](https://youtu.be/WW8_69AsBcM)

**Note**: In the video, I referred to pyRDDLGym as a "compiler." To clarify, pyRDDLGym is a simulation environment for RDDL, used in reinforcement learning applications, not a compiler.

## Installation
To get started, clone the repository and install the dependencies listed in `requirements.txt`. This project uses Python version 3.10.6.

```bash
git clone https://github.com/Tiny-Small/RDDL-Code-Generator.git
cd RDDL-Code-Generator
pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu
```

## Usage
1. Set Up the Environment:
  - Configure the `.env` file with necessary API keys:
    - `NVIDIA_API_KEY` for Nvidia embedding and reranking.
    - `OPENAI_API_KEY` for text generation
2. Creating the vector store:
```bash
cd data_processing
python run main.py
```
3. Running the Project: To start the application with the Streamlit interface:
```bash
cd querying
streamlit run app.py
```

## Data
The data used in this project is sourced from the International Probabilistic Planning Competition 2011. It provides RDDL examples that serve as a reference for generating new RDDL environments based on user-provided natural language descriptions.

## Project Structure
- `main.py`: The main script for running code generation and creating the vector store.
- `app.py`: Streamlit app for interacting with the code generator.
- `data_processing/`: Contains modules for creating the vector store
- `query/`: Contains modules for querying.
- `requirements.txt`: Lists all dependencies.

## License
This project is licensed under the [MIT License](LICENSE).
