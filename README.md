# FastAPI Logging with Correlation-ID


## Requerimentos

### uv
Install uv
https://docs.astral.sh/uv/getting-started/installation/

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Configure terminal integration:

```bash
echo 'eval "$(uv generate-shell-completion bash)"' >> ~/.bashrc
echo 'eval "$(uv generate-shell-completion zsh)"' >> ~/.zshrc

echo 'eval "$(uvx --generate-shell-completion bash)"' >> ~/.bashrc
echo 'eval "$(uvx --generate-shell-completion zsh)"' >> ~/.zshrc

source $HOME/.cargo/env
```

Install a specific version of Python:
```bash
uv python install 3.12
uv python pin 3.12
```


Install the project dependencies:

```bash
uv sync --frozen
```


## Running the project

```bash
source .venv/bin/activate
uvicorn main:app --reload
```


## Testing the project

In another terminal, use CURL to access the API's /route_one endpoint.

```bash
curl http://127.0.0.1:8000/route_one
```

The API logs should appear in the first terminal, showing the Correlation IDs maintained across calls:
```bash
INFO      [00000000-0000-0000-0000-000000000000] [Sample FastAPI App] 2024-03-08 14:14:07,785 - Application startup complete.
INFO      [67725191-13b7-4d9a-bf66-b609c081bd24] [Sample FastAPI App] 2024-03-08 14:14:11,388 - Logging from route_one()
DEBUG     [67725191-13b7-4d9a-bf66-b609c081bd24] [Sample FastAPI App] 2024-03-08 14:14:11,389 - Request called with headers: {'X-Custom': '123', 'X-Correlation-Id': '67725191-13b7-4d9a-bf66-b609c081bd24'}
INFO      [67725191-13b7-4d9a-bf66-b609c081bd24] [Sample FastAPI App] 2024-03-08 14:14:11,392 - Logging from route_two()
DEBUG     [67725191-13b7-4d9a-bf66-b609c081bd24] [Sample FastAPI App] 2024-03-08 14:14:11,392 - Request called with headers: {'X-Custom': '123', 'X-Correlation-Id': '67725191-13b7-4d9a-bf66-b609c081bd24'}
INFO      [67725191-13b7-4d9a-bf66-b609c081bd24] [Sample FastAPI App] 2024-03-08 14:14:11,395 - Logging from route_three()
INFO      [67725191-13b7-4d9a-bf66-b609c081bd24] [Sample FastAPI App] 2024-03-08 14:14:11,397 - 127.0.0.1:34190 - "GET /route_three HTTP/1.1" 200 OK
INFO      [67725191-13b7-4d9a-bf66-b609c081bd24] [Sample FastAPI App] 2024-03-08 14:14:11,399 - 127.0.0.1:34188 - "GET /route_two HTTP/1.1" 200 OK
INFO      [67725191-13b7-4d9a-bf66-b609c081bd24] [Sample FastAPI App] 2024-03-08 14:14:11,401 - 127.0.0.1:34184 - "GET /route_one HTTP/1.1" 200 OK
```

If a Correlation ID is sent in the initial request header, it is maintained in subsequent calls:
```bash
curl -H "X-Correlation-Id: c8f6a9f9-3883-42fc-be6e-5fbe365498c9" http://127.0.0.1:8000/route_one
```


## Testing the project - Communication between two services maintaining UUID across calls
To demonstrate Correlation IDs in communications between different services, start two instances of the application. Open a first terminal and run the command:
```bash
export APP_NAME="FastAPI App 001" && uvicorn main:app --reload --port=8000
```

Now, open a second terminal and run the command (notice we change the app name and port):
```bash
export APP_NAME="FastAPI App 002" && uvicorn main:app --reload --port=8001
```

Finally, in a third terminal, run the command to make a call to the second application's route:
```bash
curl -H "X-Correlation-Id: 0192ff5a-955e-7736-b36f-5700a5645ccc" http://127.0.0.1:8001/route_one
```
