import sys
import os
import uvicorn

# Insert the backend directory into sys.path to allow absolute imports of 'app' package
backend_path = os.path.dirname(os.path.abspath(__file__))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

if __name__ == "__main__":
    print("=" * 60)
    print("SAMS Production REST API Service")
    print("=" * 60)
    uvicorn.run("app.api.main:app", host="0.0.0.0", port=8000, reload=False)
