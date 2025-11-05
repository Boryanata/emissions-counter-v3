# Deploying to Hugging Face Spaces

## 📋 Pre-Deployment Checklist

### 1. **File Naming**
Hugging Face Spaces looks for `app.py` by default. You have two options:

**Option A: Rename your file (Recommended)**
```bash
mv app_dash.py app.py
```

**Option B: Configure in Space Settings**
- In your Space settings, set the "Main file" to `app_dash.py`

### 2. **Required Files**
Make sure these are in your repository:
- ✅ `app.py` (or `app_dash.py` if configured)
- ✅ `requirements.txt`
- ✅ `counter_component.py` (local module)
- ✅ `emissions_counter/` directory (local package)
- ✅ `README.md` (for Space description)

### 3. **Port Configuration**
The app is already configured to use:
- Port from `PORT` environment variable (defaults to 7860 for HF Spaces)
- Host: `0.0.0.0` (required for HF Spaces)

### 4. **Space Configuration**
When creating your Space:
- **SDK**: Select "Docker" or "Python" (not Gradio/Streamlit)
- **Hardware**: Choose based on your needs (CPU is fine for this app)
- **Visibility**: Public or Private

## 🚀 Deployment Steps

1. **Create a new Space on Hugging Face**:
   - Go to https://huggingface.co/spaces
   - Click "Create new Space"
   - Choose a name (e.g., `emissions-counter-llm`)
   - Select SDK: **Docker** or **Python**
   - Set visibility

2. **Push your code**:
   ```bash
   git remote add huggingface https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
   git push huggingface main
   ```
   
   Or upload files directly through the HF Spaces interface.

3. **Verify deployment**:
   - HF Spaces will automatically build and deploy
   - Check the "Logs" tab for any errors
   - Your app will be available at: `https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space`

## ⚙️ Important Considerations

### Port Handling
The app now checks:
1. `PORT` environment variable (if set)
2. `SPACE_PORT` environment variable (HF Spaces specific)
3. Defaults to `7860` (HF Spaces standard port)

### Local Packages
Your local packages (`emissions_counter` and `counter_component`) will be included automatically since they're in your repository.

### Dependencies
Your `requirements.txt` should include:
```
dash==2.14.2
plotly==5.17.0
pandas==2.1.4
```

### Environment Variables
You can set these in HF Spaces Settings:
- `DEBUG`: Set to `False` for production
- `PORT`: Usually auto-set by HF Spaces (don't change unless needed)

## 🔍 Troubleshooting

1. **App not loading**: Check logs in the "Logs" tab
2. **Import errors**: Make sure local packages are in the repo
3. **Port errors**: Verify port configuration in the code
4. **Build failures**: Check `requirements.txt` for compatibility

## 📝 Space README

Update your `README.md` with HF Spaces metadata at the top:
```yaml
---
title: Emissions Calculator for LLMs
emoji: 🌍
colorFrom: green
colorTo: blue
sdk: docker
sdk_version: 3
app_file: app.py
pinned: false
---
```

This helps HF Spaces understand your app configuration.

