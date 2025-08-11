#!/bin/bash
echo "Starting NextJS Frontend..."
cd frontend
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
npm run dev
