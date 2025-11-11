#!/bin/bash
# Data Preprocessing Script
# Runs XML to JSON conversion and generates embeddings cache

echo "=========================================="
echo "Data Preprocessing Pipeline"
echo "=========================================="
echo ""

# Activate virtual environment
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "⚠️  Warning: No virtual environment found"
    echo "   Continuing with system Python..."
fi

echo ""

# Step 1: XML to JSON preprocessing
echo "=========================================="
echo "Step 1: Converting XML to JSON"
echo "=========================================="
echo ""

if [ -f "knowledge_base/legislation_database.json" ]; then
    echo "⚠️  legislation_database.json already exists"
    read -p "Rebuild? (y/N): " REBUILD_JSON
    REBUILD_JSON=${REBUILD_JSON:-N}
    
    if [[ $REBUILD_JSON =~ ^[Yy]$ ]]; then
        echo "Rebuilding JSON database..."
        python3 -m knowledge_base.preprocess_legislation
    else
        echo "Skipping JSON conversion"
    fi
else
    echo "Creating JSON database..."
    python3 -m knowledge_base.preprocess_legislation
fi

echo ""

# Check if JSON was created successfully
if [ ! -f "knowledge_base/legislation_database.json" ]; then
    echo "❌ Error: legislation_database.json was not created"
    echo "   Please check for errors above"
    exit 1
fi

echo "✅ JSON database ready"
echo ""

# Step 2: Generate embeddings
echo "=========================================="
echo "Step 2: Generating Embeddings"
echo "=========================================="
echo ""

if [ -d "knowledge_base/cached_embeddings" ] && [ -f "knowledge_base/cached_embeddings/legislation_embeddings.npy" ]; then
    echo "⚠️  Embeddings cache already exists"
    read -p "Rebuild? (y/N): " REBUILD_EMBEDDINGS
    REBUILD_EMBEDDINGS=${REBUILD_EMBEDDINGS:-N}
    
    if [[ $REBUILD_EMBEDDINGS =~ ^[Yy]$ ]]; then
        echo "Rebuilding embeddings..."
        python3 -m knowledge_base.embeddings_index --rebuild
    else
        echo "Skipping embeddings generation"
        echo "Loading existing embeddings for testing..."
        python3 -m knowledge_base.embeddings_index --no-test
    fi
else
    echo "Generating embeddings (this will take 5-10 minutes)..."
    python3 -m knowledge_base.embeddings_index
fi

echo ""

# Check if embeddings were created successfully
if [ ! -d "knowledge_base/cached_embeddings" ]; then
    echo "❌ Error: Embeddings cache was not created"
    echo "   Please check for errors above"
    exit 1
fi

echo "✅ Embeddings cache ready"
echo ""

# Summary
echo "=========================================="
echo "✅ Preprocessing Complete!"
echo "=========================================="
echo ""

# Show file sizes
JSON_SIZE=$(du -h knowledge_base/legislation_database.json | cut -f1)
CACHE_SIZE=$(du -sh knowledge_base/cached_embeddings | cut -f1)

echo "📊 Data Summary:"
echo "   JSON Database: $JSON_SIZE"
echo "   Embeddings Cache: $CACHE_SIZE"
echo ""

echo "Next steps:"
echo "1. Run ./setup_rag.sh to install Ollama and LLaMA"
echo "2. Start the application with ./run.sh"
echo ""

