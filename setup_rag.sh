#!/bin/bash
# Setup script for RAG system
# Installs Ollama and pulls LLaMA model

echo "=========================================="
echo "RAG System Setup"
echo "=========================================="
echo ""

# Check if Ollama is installed
echo "Checking for Ollama installation..."
if command -v ollama &> /dev/null; then
    echo "✅ Ollama is already installed"
    OLLAMA_VERSION=$(ollama --version)
    echo "   Version: $OLLAMA_VERSION"
else
    echo "❌ Ollama not found"
    echo ""
    echo "Installing Ollama..."
    
    # Detect OS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "Detected macOS"
        echo "Please visit: https://ollama.ai/download"
        echo "Download and install Ollama for macOS"
        echo ""
        echo "After installation, run this script again."
        exit 1
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "Detected Linux"
        curl -fsSL https://ollama.ai/install.sh | sh
    else
        echo "Unsupported operating system: $OSTYPE"
        echo "Please visit https://ollama.ai/download for manual installation"
        exit 1
    fi
fi

echo ""

# Check if Ollama service is running
echo "Checking Ollama service..."
if pgrep -x "ollama" > /dev/null; then
    echo "✅ Ollama service is running"
else
    echo "⚠️  Ollama service is not running"
    echo "Starting Ollama service in background..."
    ollama serve > /dev/null 2>&1 &
    sleep 3
    echo "✅ Ollama service started"
fi

echo ""

# Pull LLaMA models
echo "=========================================="
echo "Downloading LLaMA Models"
echo "=========================================="
echo ""

echo "Choose which model to download:"
echo "1) llama3.2:3b (2GB, faster, good for testing)"
echo "2) llama3.1:8b (4.7GB, better quality, recommended)"
echo "3) Both models"
echo ""
read -p "Enter choice (1-3) [default: 2]: " MODEL_CHOICE
MODEL_CHOICE=${MODEL_CHOICE:-2}

case $MODEL_CHOICE in
    1)
        echo "Pulling llama3.2:3b model..."
        ollama pull llama3.2:3b
        echo "✅ Model downloaded: llama3.2:3b"
        ;;
    2)
        echo "Pulling llama3.1:8b model..."
        ollama pull llama3.1:8b
        echo "✅ Model downloaded: llama3.1:8b"
        ;;
    3)
        echo "Pulling both models..."
        ollama pull llama3.2:3b
        echo "✅ Model downloaded: llama3.2:3b"
        ollama pull llama3.1:8b
        echo "✅ Model downloaded: llama3.1:8b"
        ;;
    *)
        echo "Invalid choice. Pulling llama3.1:8b (recommended)..."
        ollama pull llama3.1:8b
        echo "✅ Model downloaded: llama3.1:8b"
        ;;
esac

echo ""

# Test Ollama
echo "=========================================="
echo "Testing Ollama"
echo "=========================================="
echo ""

echo "Running test query..."
TEST_RESPONSE=$(ollama run llama3.1:8b "Say 'Hello from Ollama!' and nothing else" 2>&1 | head -n 1)
echo "Response: $TEST_RESPONSE"

if [[ $TEST_RESPONSE == *"Hello"* ]]; then
    echo "✅ Ollama is working correctly!"
else
    echo "⚠️  Ollama test may have issues"
    echo "   Full response: $TEST_RESPONSE"
fi

echo ""

# List available models
echo "=========================================="
echo "Available Models"
echo "=========================================="
ollama list

echo ""
echo "=========================================="
echo "✅ RAG Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Ensure you've run: python3 -m knowledge_base.preprocess_legislation"
echo "2. Ensure you've run: python3 -m knowledge_base.embeddings_index"
echo "3. Test the RAG engine with sample queries"
echo ""
echo "To start the Flask app with RAG enabled:"
echo "  ./run.sh"
echo ""

