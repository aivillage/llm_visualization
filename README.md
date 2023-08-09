# llm_visualization
This is a visualization tool to teach people about LLMs. It works in tandem with a [visualization UI](https://github.com/zgordon01/aivillage-llm-visualization-ui)

Please note that CORS is essentially disabled, so that must be addressed before hosting this anywhere.

# First, Install Dependencies
`pip install -r requirements.txt`

## Running Locally
1. Run the dev server: `cd app;uvicorn api:app --reload`

## Running in Docker
1. From project root, build the image: `docker build --tag llm-visualization .`
2. Create a container from the image: `docker run -p 8000:8000 llm-visualization`. We are exposing port 8000 for the UI.

Note that this uses a substantial amount of memory, ensure that docker has ~10GB+ available to it.