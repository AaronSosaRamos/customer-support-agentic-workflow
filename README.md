# Customer Support Agentic Workflow
## Made by: Wilfredo Aaron Sosa Ramos


1. Ensure Qdrant is running:
The app expects Qdrant to be running on localhost:6333. Adjust the configuration in the code if your setup is different.

```bash
docker pull qdrant/qdrant

docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant
```

On Windows:

```bash
docker run -p 6333:6333 -p 6334:6334 -v C:/Users/YourUserName/Documents/qdrant_storage:/qdrant/storage:z qdrant/qdrant
```

2. Run the Streamlit App
```bash
streamlit run main.py
```