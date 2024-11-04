# AI Bootcamp IM8

## Python version

3.12.6

# Development Runbook

## Initial Setup

1. **Clone the repository**
   ```bash
   git clone git@sgts.gitlab-dedicated.com:destin_ngeow1/ai-bootcamp-im8.git
   cd ai-bootcamp-im8
   ```
2. **Install Python**
   Ensure that the Python version `3.12.6` is installed on your system.
   (Optional) It's recommended to use a Python version manager to help manage your local Python environment. For example `pyenv`.
3. **Setting Up a Local Python Virtual Environment**
   ```bash
   python3 -m venv venv
   ```
4. **Activate the virtual environment**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS
     ```bash
     source venv/bin/activate
     ```
5. **Install dependencies**
   ```bash
   pip install --upgrade -r requirements.txt
   ```
6. **Set up environment variables**
   Create a folder `.streamlit` and a `secrets.toml` file in the `.streamlit` folder, copy the content from `secrets.toml.example` and replace the value accordingly.

### Environment Variables

| Name              | Description                               | Default     |
| ----------------- | ----------------------------------------- | ----------- |
| OPENAI_API_KEY    | OpenAI Key                                | none        |
| OPENAI_MODEL_NAME | Name of the OpenAI model you wish to use. | gpt-4o-mini |
| PINECONE_API_KEY  | Pinecone API Key                          | none        |
| PASSWORD          | Password to access app                    | none        |

## Initial Data Preparations for Web App

The data preperation needs to be run once before running the application.

1. Go to github repository https://github.com/GovTechSG/tech-standards and copy the `catalog` and `profiles` folders into the root directory of this project.
2. Run `python prep.py`

### Notes:

As this is still in the initial testing phase, the vector DB is only using a local persistant folder `vector_db`. Consider moving to proper vector DB host by infra.

Some of the import paths, assumes that the application is run from the root folder of the project. Consider changing it to be more dynamic depending on deployment needs.

## Running Application in Development on local machine

- Ensure that the initial setup steps are completed.
- Note that you likely need to turn off SEED.
- Run `streamlit run app/main.py`
