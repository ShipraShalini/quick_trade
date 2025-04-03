# 📈 Stock Exchange Order API

This project is a high-performance order processing backend built with **FastAPI**, **Tortoise ORM**, and **asyncpg** for asynchronous PostgreSQL interactions.

It provides a minimal but functional structure to handle order placement and interaction with stock exchanges. While the current implementation is synchronous in parts, it's designed to evolve into a scalable and production-grade system.

---

## 🚀 Features

- 🌀 **Async API** using FastAPI and asyncpg
- 🐢 **Tortoise ORM** for non-blocking DB interactions
- 🧾 Modular code organization: orders, stock exchanges, responses, exceptions
- 🔁 A planned **periodic task** system to retry failed orders
- ⚙️ Configuration via Python settings module
- 📄 Auto-generated Swagger docs for API testing

---

## 🛠 Assumptions & Current Behavior

- There is a placeholder for a periodic task that retries orders that failed to be placed.
- The `place_order` function is called directly from the API route, which can block the request if it's slow.
- At the moment, there is **no queuing system** — the order placement runs in-line and may slow down responses.
- If `place_order` fails, it is retried manually via a planned periodic job.

---

## 🔮 Planned Improvements

Here are some of the areas identified for enhancement:

1. **Task Queue Integration**
   - Introduce **Celery** or **RQ** to offload `place_order` calls to a background worker.
   - Add retry logic with **backoff and jitter** to gracefully handle failures.

2. **Background Tasks**
   - Use FastAPI's `BackgroundTasks` as a lightweight stopgap to avoid blocking the request thread.

3. **Scalability**
   - Introduce **API versioning** for long-term compatibility and extensibility.
   - Separate read and write concerns for better performance under load.

4. **Security**
   - Currently, there is **no authentication or authorization**.
   - Plan to add JWT-based or OAuth2 security in the future.

5. **Monitoring and Alerting**
   - Integrate logging, metrics, and tracing to monitor the API and background workers.

---


## Steps to run using docker-compose:
1. Unzip the project directory.
2. Set up the following env variables:
    ```Shell
    export ENVIRONMENT=<your-environment>  # can be local or production
    export SECRET_KEY=<your-secret-key>    # not used forRun the services using Docker Compose: docker-compose up
   ```
3. Run the services using Docker Compose: `docker-compose up`
4. Run migrations
    ```shell
    docker exec -it exercise-backend-main-quik_trade-1 aerich upgrade
    ```

## Steps to run with uvicorn
Assumes that postgres is running and setup properly, you can also use docker-compose to run the db.
1. Create a virtualenv and activate it.
    ```shell
   virtualenv venv -p python3.12
   activate
   ```
2. Install app in editable mode
    ```shell
    pip install -e . -r requirements-dev.txt
   ```
3. Run migrations
   ```shell
   aerich upgrade
   ```
4. Run with uvicorn
   ```shell
   uvicorn app.api:app --reload
   ```

## Steps to run tests
1. Create a virtualenv and activate it.
    ```shell
   virtualenv venv -p python3.12
   activate
   ```
2. Install app in editable mode
    ```shell
    pip install -e . -r requirements-dev.txt
   ```
3. Install dev dependencies
    ```shell
    pip install -r requirements-dev.txt
   ```
4. Run tests with pytest
   ```shell
   pytest -s
   ```
