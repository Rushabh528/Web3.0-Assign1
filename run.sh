PYTHON_SCRIPT="main.py"

find_python() {
    echo "python"
}

PYTHON=$(find_python)

if [ -z "$PYTHON" ]; then
    echo "Python is not installed or not found in the PATH. Please install Python or adjust your PATH settings."
    exit 1
fi

echo "Running the Python script with $PYTHON..."
$PYTHON $PYTHON_SCRIPT
