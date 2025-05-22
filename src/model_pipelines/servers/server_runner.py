import asyncio
import grpc


async def run_grpc_server(servicer_cls, add_servicer_fn, port: int):
    server = grpc.aio.server()
    add_servicer_fn(servicer_cls(), server)

    server_address = f"[::]:{port}"
    server.add_insecure_port(server_address)

    await server.start()
    print(f"✅ gRPC server running on {server_address}. Press Ctrl+C or Stop to exit.")

    try:
        await server.wait_for_termination()
    except (asyncio.CancelledError, KeyboardInterrupt):
        print("⚠️ Shutdown initiated. Stopping server...")
        try:
            await server.stop(grace=None)
        except asyncio.CancelledError:
            print("⚠️ Forced exit before full shutdown.")
        print("🛑 gRPC server shut down.")