import sys
import os

# Fix for PyInstaller --noconsole mode where stdout/stderr are None
# This prevents uvicorn/logging from crashing with AttributeError: 'NoneType' object has no attribute 'isatty'
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Body
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import pandas as pd
import numpy as np
import io
import logging
from typing import List, Optional, Dict

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    return os.path.join(base_path, relative_path)

# Add backend directory to path to import data_processor
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_processor import (
    load_data, merge_datasets, calculate_stats, downsample_for_plot, 
    calculate_correlations, parse_legend, filter_columns, 
    calculate_derived_var, get_stability_bands, process_extra_dataset
)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_dir = get_resource_path(os.path.join("frontend", "static"))
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Global storage
# In a real multi-user app, this would be a database or session-based storage (e.g. Redis)
current_df: Optional[pd.DataFrame] = None
data_files: Dict[str, pd.DataFrame] = {}
legend_data: Dict[str, Dict] = {}

@app.get("/")
async def read_root():
    # In a real app, use Jinja2 templates. For now, read the file and return.
    pixel_path = get_resource_path(os.path.join("frontend", "templates", "index.html"))
    if os.path.exists(pixel_path):
        with open(pixel_path, 'r', encoding='utf-8') as f:
            return HTMLResponse(content=f.read())
    return {"message": "Backend is running. Frontend index.html not found."}

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    global data_files, legend_data
    uploaded_names = []
    
    for file in files:
        try:
            content = await file.read()
            
            # Check if it's a legend file based on name
            if 'legend' in file.filename.lower() and file.filename.endswith('.csv'):
                legend_data = parse_legend(content)
                uploaded_names.append(f"{file.filename} (Legend)")
            else:
                # Load data file
                df = load_data(content, file.filename)
                data_files[file.filename] = df
                uploaded_names.append(file.filename)
        except Exception as e:
            logging.error(f"Failed to process {file.filename}: {e}")
            return JSONResponse(status_code=400, content={"message": f"Failed to process {file.filename}: {str(e)}"})
            
    return {"message": "Files uploaded successfully", "files": uploaded_names}

@app.post("/upload-legend")
async def upload_legend(file: UploadFile = File(...)):
    global legend_data
    try:
        content = await file.read()
        legend_data = parse_legend(content)
        return {"message": "Legend uploaded successfully", "entries": len(legend_data)}
    except Exception as e:
        logging.error(f"Failed to process legend {file.filename}: {e}")
        return JSONResponse(status_code=400, content={"message": f"Failed to process legend: {str(e)}"})

@app.post("/process")
async def process_data(
    min_nonzero: float = Form(0.0),
    merge_strategy: str = Form('linear')
):
    global current_df, data_files
    
    if not data_files:
        return JSONResponse(status_code=400, content={"message": "No files uploaded"})
    
    try:
        # Sort files? for now take values
        dfs = list(data_files.values())
        
        # Merge
        merged = merge_datasets(dfs, interpolation_method=merge_strategy)
        
        # Filter
        if min_nonzero > 0:
            merged = filter_columns(merged, min_nonzero_pct=min_nonzero)
            
        # Clean column names in merged df
        merged.columns = merged.columns.astype(str).str.replace(' ', '_')
        
        current_df = merged
        
        return {"message": "Data merged successfully", "rows": len(current_df), "columns": list(current_df.columns)}
    except Exception as e:
        logging.error(f"Merge failed: {e}")
        return JSONResponse(status_code=500, content={"message": str(e)})

@app.post("/add-dataset")
async def add_dataset(
    file: UploadFile = File(...),
    method: str = Form('linear'),
    gap_limit: Optional[float] = Form(None),
    suffix: str = Form('')
):
    global current_df, data_files
    if current_df is None:
        return JSONResponse(status_code=400, content={"message": "No active dataset to merge into."})
        
    try:
        content = await file.read()
        
        # We don't necessarily add to data_files unless we want to persist it for re-process (which resets current_df).
        # But here we are modifying current_df directly as an additive step.
        # Ideally we should add to data_files and re-merge, but this endpoint implies "add ON TOP of current result".
        # Let's modify current_df.
        
        current_df = process_extra_dataset(
            current_df, 
            content, 
            file.filename, 
            method=method, 
            gap_limit=gap_limit, 
            suffix=suffix
        )
        
        return {"message": f"Dataset {file.filename} added.", "columns": list(current_df.columns)}
    except Exception as e:
        logging.error(f"Add dataset failed: {e}")
        return JSONResponse(status_code=500, content={"message": str(e)})

@app.post("/add-derived")
async def add_derived_variable(
    name: str = Form(...),
    formula: str = Form(...),
    unit: Optional[str] = Form(None),
    min_val: Optional[str] = Form(None),
    max_val: Optional[str] = Form(None)
):
    global current_df, legend_data
    if current_df is None:
        return JSONResponse(status_code=400, content={"message": "No data active"})
        
    try:
        current_df = calculate_derived_var(current_df, name, formula)
        
        # Update legend metadata if provided
        if unit or min_val or max_val:
            if name not in legend_data:
                legend_data[name] = {}
            
            if unit: legend_data[name]['Unit'] = unit
            if min_val: legend_data[name]['Scale min'] = min_val
            if max_val: legend_data[name]['Scale max'] = max_val
            
        return {"message": f"Variable {name} added", "columns": list(current_df.columns)}
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

@app.get("/columns")
async def get_columns():
    global current_df
    if current_df is None:
        return {"columns": []}
    return {"columns": list(current_df.columns)}

@app.get("/stats")
async def get_stats():
    global current_df
    if current_df is None:
        return JSONResponse(status_code=400, content={"message": "No data processed"})
    
    try:
        stats = calculate_stats(current_df)
        return {"stats": stats}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

@app.get("/legend")
async def get_legend():
    global legend_data
    return {"legend": legend_data}

@app.post("/plot-data")
async def get_plot_data(
    x_var: str = Form(...), 
    y_vars: List[str] = Form(...),
    max_points: int = Form(5000)
):
    global current_df
    if current_df is None:
        return JSONResponse(status_code=400, content={"message": "No data active"})
    
    try:
        # Filter columns
        cols = [x_var] + y_vars
        # Remove duplicates
        cols = list(set(cols))
        
        # Check existence
        missing = [c for c in cols if c not in current_df.columns]
        if missing:
             return JSONResponse(status_code=400, content={"message": f"Columns not found: {missing}"})

        subset = current_df[cols].copy()
        subset = subset.dropna()
        
        # Downsample
        sampled = downsample_for_plot(subset, max_points)
        
        # Convert to records
        if 'timestamp' in sampled.columns:
            sampled['timestamp'] = sampled['timestamp'].astype(str)
            
        data = sampled.to_dict(orient='list')
        return {"data": data}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

@app.get("/bands/{var_name}")
async def get_bands(var_name: str):
    global current_df
    if current_df is None:
        return JSONResponse(status_code=400, content={"message": "No data active"})
        
    try:
        bands = get_stability_bands(current_df, var_name)
        return {"bands": bands}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

@app.get("/heatmap")
async def get_heatmap(method: str = 'pearson'):
    global current_df
    if current_df is None:
        return JSONResponse(status_code=400, content={"message": "No data active"})
    
    try:
        heat = calculate_correlations(current_df, method=method)
        return heat
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

@app.post("/ai-query")
async def ai_query(
    query: str = Form(...),
    context: str = Form(...),
    api_key: Optional[str] = Form(None),
    provider: str = Form("openai"),
    base_url: Optional[str] = Form(None)
):
    import requests
    try:
        if provider == "gemini":
            if not api_key:
                return JSONResponse(status_code=400, content={"message": "API Key required for Gemini provider"})
            
            # Using Gemini 1.5 Flash via REST API
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key.strip()}"
            headers = { "Content-Type": "application/json" }
            payload = {
                "contents": [{
                    "parts": [{
                        "text": f"System: You are a data analysis assistant for kiln process monitoring.\nContext:\n{context}\n\nQuery: {query}"
                    }]
                }]
            }
            logging.info(f"Sending AI Query to Gemini API")
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if not response.ok:
                error_msg = f"Gemini Error ({response.status_code}): {response.text}"
                logging.error(error_msg)
                return JSONResponse(status_code=response.status_code, content={"message": error_msg})
            
            res_json = response.json()
            try:
                content = res_json['candidates'][0]['content']['parts'][0]['text']
                # Normalize to match OpenAI format for frontend
                return {"choices": [{"message": {"content": content}}]}
            except (KeyError, IndexError) as e:
                return JSONResponse(status_code=500, content={"message": f"Malformed Gemini response: {str(e)}"})
                
        elif provider == "custom":
            if not base_url:
                return JSONResponse(status_code=400, content={"message": "Base URL required for custom provider"})
            
            headers = { "Content-Type": "application/json" }
            if api_key:
                headers["Authorization"] = f"Bearer {api_key.strip()}"
            
            payload = {
                "model": "gpt-4o", # Assume default or proxy-defined model
                "messages": [
                    {"role": "system", "content": "You are a data analysis assistant."},
                    {"role": "user", "content": f"Context:\n{context}\n\nQuery: {query}"}
                ],
                "max_tokens": 1000
            }
            logging.info(f"Sending AI Query to custom endpoint: {base_url}")
            response = requests.post(base_url, headers=headers, json=payload, timeout=30)
            
            if not response.ok:
                error_msg = f"Custom Provider Error ({response.status_code}): {response.text}"
                logging.error(error_msg)
                return JSONResponse(status_code=response.status_code, content={"message": error_msg})
                
            return response.json()

        else: # Default OpenAI
            if not api_key:
                return JSONResponse(status_code=400, content={"message": "API Key required for OpenAI provider"})
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key.strip()}"
            }
            payload = {
                "model": "gpt-4o",
                "messages": [
                    {"role": "system", "content": "You are a data analysis assistant."},
                    {"role": "user", "content": f"Context:\n{context}\n\nQuery: {query}"}
                ],
                "max_tokens": 1000
            }
            logging.info("Sending AI Query to OpenAI API")
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=30)
            
            if not response.ok:
                error_msg = f"OpenAI Error ({response.status_code}): {response.text}"
                logging.error(error_msg)
                return JSONResponse(status_code=response.status_code, content={"message": error_msg})
                
            return response.json()
            
    except Exception as e:
        logging.error(f"AI Query Exception: {str(e)}", exc_info=True)
        return JSONResponse(status_code=500, content={"message": f"Unexpected backend error: {str(e)}"})

@app.get("/export-data")
async def export_data(format: str = "csv"):
    global current_df
    if current_df is None:
        return JSONResponse(status_code=400, content={"message": "No data active"})
    
    try:
        if format.lower() == "csv":
            stream = io.StringIO()
            current_df.to_csv(stream, index=False)
            response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
            response.headers["Content-Disposition"] = "attachment; filename=export.csv"
            return response
        elif format.lower() == "xlsx":
            stream = io.BytesIO()
            # engine='openpyxl' is default for xlsx usually, but good to specify or let pandas decide
            current_df.to_excel(stream, index=False, engine='openpyxl')
            stream.seek(0)
            response = StreamingResponse(stream, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response.headers["Content-Disposition"] = "attachment; filename=export.xlsx"
            return response
        else:
            return JSONResponse(status_code=400, content={"message": "Invalid format. Use csv or xlsx."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
