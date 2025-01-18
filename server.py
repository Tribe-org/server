import uvicorn


def main():
    PORT_NUMBER = 8888
    print(f"Server Start!! {PORT_NUMBER}")
    uvicorn.run(
        app="app.main:app",
        host="127.0.0.1",
        log_level="info",
        port=PORT_NUMBER,
        reload=True,
    )


if __name__ == "__main__":
    main()
