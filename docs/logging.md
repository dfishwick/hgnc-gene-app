# Logging

The app logs to the terminal (the stream) and to a rotating log file. Each has its own level, which can be set with environment variables:

- `HGNC_STREAM_LOG_LEVEL`: level for the terminal. Default `INFO`.
- `HGNC_FILE_LOG_LEVEL`: level for the log file. Default `DEBUG`.
- `HGNC_LOG_FILE`: path of the log file, used exactly as given. If it is not set, the app uses a file in the `.hgnc_gene_app` folder in the user's home folder, named with the date and time it was first made, for example `hgnc_gene_app_2026-11-01_04-25-00.log`. Later runs add to that file.

Valid levels are `DEBUG`, `INFO`, `WARNING`, `ERROR` and `CRITICAL`. An invalid level stops the app with an error message naming the variable.

The log file is rotated at 500,000 bytes and the 5 most recent older files are kept (the file name followed by `.1` to `.5`), so the logs cannot fill the disk. If the log file cannot be created, the app warns and logs to the terminal only.

Unexpected errors while handling a request are logged at `ERROR` level with the full traceback. The user sees a plain error page without the details.

To show debug messages in the terminal in PowerShell, set the variable before starting the app:

```$env:HGNC_STREAM_LOG_LEVEL = "DEBUG"```

In bash:

```export HGNC_STREAM_LOG_LEVEL=DEBUG```

With Docker, pass a variable with `-e`, for example `-e HGNC_STREAM_LOG_LEVEL=DEBUG`. Inside the container the log file is in `/root/.hgnc_gene_app/` and is deleted with the container (`--rm`), so use the terminal output or `docker logs` there.
