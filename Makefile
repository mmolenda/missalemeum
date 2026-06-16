.PHONY: help backend frontend dev run-backend run-frontend

PYTHON := ./.venv/bin/python3
API_URL := http://localhost:8000

help:
	@printf '%s\n' \
		'Available targets:' \
		'  make backend       Run the backend API on port 8000' \
		'  make frontend      Run the Next.js frontend dev server' \
		'  make dev           Run backend and frontend together' \
		'  make run-backend   Alias for backend' \
		'  make run-frontend  Alias for frontend'

backend:
	cd backend && MISSAL_NO_CACHE=True ../$(PYTHON) -m api.app

frontend:
	cd frontend && API_URL=$(API_URL) NEXT_PUBLIC_API_URL=$(API_URL) npm run dev

dev:
	$(MAKE) -j2 backend frontend

run-backend: backend

run-frontend: frontend
