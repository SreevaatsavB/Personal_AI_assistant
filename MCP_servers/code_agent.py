from typing import Any, Dict, List
import os
import json
import subprocess
import logging
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from anthropic import Anthropic
from dotenv import load_dotenv

# ——— Setup ———
load_dotenv()
API_KEY = os.getenv("ANTHROPIC_API_KEY")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("coding_agent")


mcp = FastMCP("python-backend-coder")
anthropic = Anthropic(api_key=API_KEY)




# ——— Filesystem Tools ———
@mcp.tool()
def create_directory(path: str) -> str:
    """Create directories recursively for a given path"""
    Path(path).mkdir(parents=True, exist_ok=True)
    return f"Directory created: {path}"


@mcp.tool()
def create_file(path: str, content: str) -> str:
    """Create or overwrite a file with content for a given path"""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding='utf-8')
    return f"File written: {path}"

# ——— Execution Tool ———
@mcp.tool()
def run_script(
    script_path: str,
    args: List[str] = []
) -> Dict[str, Any]:
    """
    Runs a Python script in subprocess, capturing stdout/stderr.

    Returns {"stdout": ..., "stderr": ..., "returncode": ...}
    """
    cmd = ["python", script_path] + args
    proc = subprocess.run(
        cmd, capture_output=True, text=True
    )
    return {
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "returncode": proc.returncode
    }


# @mcp.tool()
# def read_file(path: str, encoding: str = 'utf-8') -> Dict[str, Any]:
#     """
#     Read a file and return its contents as a string.
    
#     Args:
#         path: Path to the file to read
#         encoding: File encoding (default: utf-8)
        
#     Returns:
#         Dict with 'content' if successful or 'error' if failed
#     """
#     try:
#         content = Path(path).read_text(encoding=encoding)
#         return {
#             "success": True,
#             "content": content,
#             "path": path
#         }
#     except FileNotFoundError:
#         return {
#             "success": False,
#             "error": f"File not found: {path}",
#             "path": path
#         }
#     except IsADirectoryError:
#         return {
#             "success": False,
#             "error": f"Path is a directory, not a file: {path}",
#             "path": path
#         }
#     except UnicodeDecodeError:
#         return {
#             "success": False,
#             "error": f"File could not be decoded with encoding '{encoding}'. Try a different encoding.",
#             "path": path
#         }
#     except Exception as e:
#         return {
#             "success": False,
#             "error": f"Error reading file {path}: {str(e)}",
#             "path": path
#         }




# @mcp.tool()
# def copy_file(source_path: str, destination_path: str, overwrite: bool = False) -> str:
#     """
#     Copy a file from source_path to destination_path.
#     If overwrite=False, will not overwrite existing files.
#     If overwrite=True, will replace existing files.
#     """
#     source = Path(source_path)
#     destination = Path(destination_path)
    
#     try:
#         # Check if source exists and is a file
#         if not source.exists():
#             return f"Source file not found: {source_path}"
#         if not source.is_file():
#             return f"Source is not a file: {source_path}"
            
#         # Create destination directory if it doesn't exist
#         destination.parent.mkdir(parents=True, exist_ok=True)
        
#         # Check if destination exists and overwrite is False
#         if destination.exists() and not overwrite:
#             return f"Destination file already exists. Use overwrite=True to replace: {destination_path}"
            
#         # Copy the file (using shutil for more robust copying)
#         import shutil
#         shutil.copy2(source, destination)  # copy2 preserves metadata
        
#         return f"File copied: {source_path} → {destination_path}"
        
#     except Exception as e:
#         return f"Error copying file from {source_path} to {destination_path}: {str(e)}"



# ——— Deployment Tool ———
# @mcp.tool()
# def deploy_fastapi(app_dir: str, host: str="0.0.0.0", port: int=8022) -> str:
#     """
#     Launch uvicorn in background and return the endpoint URL.
#     (In production, swap for Docker or Gunicorn deploy commands.)
#     """
#     # Change working dir
#     os.chdir(app_dir)
#     # Launch uvicorn (non-blocking)
#     subprocess.Popen([
#         "uvicorn", "main:app",
#         "--host", host, "--port", str(port)
#     ])
#     return f"http://{host}:{port}/docs"



if __name__ == "__main__":
    mcp.run()
