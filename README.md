# Textual IPC

A simple proof-of-concept showing the implementation of an application spawning two processes:

* One for the UI, under [Textual](https://github.com/Textualize/textual).
* One for the background process to offload heavy blocking operations while keeping the UI responsive.

Both communicate through a Unix socket.

## License

MIT
