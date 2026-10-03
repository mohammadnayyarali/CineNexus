# Deployment

For local use, build the artifact on the host and run Uvicorn. The Docker image installs dependencies, runs as a non-root user, and serves port 8000. Mount `data/` read-only in Compose so the process can read an artifact without modifying the catalog.

The artifact is a serialized build output and should be versioned outside Git for large catalogs. Record the dataset version, configuration, Python version, and build timestamp alongside the artifact in a production registry.
