#!/bin/bash

# Build the tool-manager image
echo "Building tool-manager image..."
docker build -t tool-manager-api:latest .

echo "Tool-manager image built successfully: tool-manager-api:latest"
echo "You can now run the complete system with: docker-compose up -d"
echo ""
echo "Alternatively, to run just the tool-manager for testing, use:"
echo "docker run -p 8000:8000 tool-manager-api:latest" 