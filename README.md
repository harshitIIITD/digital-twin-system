# Digital Twin System

This project is a digital twin system that integrates various components for simulation, data integration, and machine learning. It is built using FastAPI for the backend and a frontend dashboard.

## Project Structure

```
backend/
	.env
	api/
		rest/
		v1/
	auth/
		jwt.py
	core/
		auth.py
		config.py
	data_integration/
		collectors/
		pipeline/
		storage/
	db/
		crud.py
		database.py
		init_db.py
	Dockerfile

	main.py

	middleware/

	compliance.py

	ml/
		pipeline.py
	modeling/
		physiological/
	models/
	schemas/
	security/
	simulation/
digital-twin-system/
	backend/
	frontend/

docker-compose.yml

frontend/
	.env
	dashboard/
	package.json
	src/

report.md

requirements.txt

venv/
	bin/
	include/
	lib/
	lib64
	pyvenv.cfg
```

## Backend

The backend is built using FastAPI and includes various modules for handling authentication, data integration, machine learning, and simulation.

### Key Components

- **Authentication**: JWT-based authentication is implemented in `jwt.py` and `auth.py`.
- **Data Integration**: Collects and processes data from various sources. Key files include:
  - `collectors`
  - `pipeline`
  - `storage`
- **Machine Learning**: Handles ML model pipelines in `pipeline.py`.
- **Modeling**: Physiological models are implemented in `physiological`.
- **Simulation**: Simulation engine and endpoints are in `simulation`.
- **Middleware**: Compliance middleware for security headers and logging in `compliance.py`.

### API Endpoints

- **Simulation**: Run simulations for patients.
  - `simulation.py`

- **Data Integration**: Collect and retrieve patient data.
  - `data_integration.py`

### Configuration

Configuration settings are managed in `config.py`.

### Database

Database initialization and CRUD operations are handled in:
- `init_db.py`
- `crud.py`
- `database.py`

### Running the Backend

To run the backend, use Docker:

```sh
docker-compose up --build
```

Alternatively, you can run it locally:

```sh
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Frontend

The frontend is a dashboard built with modern web technologies.

### Running the Frontend

To run the frontend, navigate to the `frontend` directory and use npm:

```sh
cd frontend
npm install
npm start
```

## Virtual Environment

Activate the virtual environment using the provided script:

```sh
source venv/bin/activate
```

For PowerShell:

```ps1
.\venv\bin\Activate.ps1
```

## Health Check

Check the health of the backend service:

```sh
curl http://localhost:8000/health
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please see the CONTRIBUTING file for more information.

## Contact

For any inquiries, please contact the project maintainers.

---

This README provides an overview of the project structure, key components, and instructions for running the backend and frontend services.
