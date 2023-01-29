import asyncio
from datetime import datetime

async def handle_echo(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')

    print(f"Received {message!r} from {addr!r}")
    if message.startswith('/'):
        while True:
            if message == '/date':
                message = datetime.now()
                print(f"Send: {message!r}")

            elif message == '/hello':
                message = 'hello'
                print(f"Send: {message!r}")

            elif message == '/goodbye':
                message = 'goodbye'
                print(f"Send: {message!r}")

            else:
                print(f'Send: this command {message!r} does not exist')
                break

    else:
        print(f"Send: {message!r}")
        writer.write(data)
        await writer.drain()

    message = str(message).encode()
    writer.write(message)
    await writer.drain()
    print("Close the connection")
    writer.close()

async def main():
    server = await asyncio.start_server(
        handle_echo, '127.0.0.1', 7777)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

asyncio.run(main())