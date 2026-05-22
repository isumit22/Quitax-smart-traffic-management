# Quitax Smart Traffic Management

This repository contains a small demo AI-driven traffic signal controller.

Quick start (Windows PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# Start backend
python backend\app.py
# Serve frontend
python -m http.server 8000 --directory frontend
```

Notes
- Ensure `videos/` contains `video1.mp4` .. `video4.mp4` or update paths in `backend/app.py`.
- Place the `yolov8n.pt` model file inside `backend/` (it will be loaded lazily).
- The `/health` endpoint reports whether the app is up and whether the model has been loaded.

Recommended next steps
- Pin exact `torch` wheel for your platform (CPU vs GPU). See https://pytorch.org for install commands.
- Consider adding logging, tests, and async inference queue for production usage.
