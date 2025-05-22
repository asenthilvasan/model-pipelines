import asyncio
import signal
import grpc

async def run_grpc_server(servicer_cls, add_servicer_fn, port: int):
    """
    Starts and gracefully shuts down an async gRPC server.

    Args:
        servicer_cls: The class implementing your gRPC service (e.g., ControllerService).
        add_servicer_fn: The generated gRPC function to bind the service (e.g., add_ControllerServiceServicer_to_server).
        port (int): The port to listen on (e.g., 50053).
    """
    server = grpc.aio.server()
    add_servicer_fn(servicer_cls(), server)
    server.add_insecure_port(f"[::]:{port}")
    await server.start()

    print(f"✅ gRPC server running on port {port}. Press Ctrl+C to stop.")

    shutdown_event = asyncio.Event()

    def handle_shutdown():
        shutdown_event.set()

    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGINT, handle_shutdown)
    loop.add_signal_handler(signal.SIGTERM, handle_shutdown)

    await shutdown_event.wait()

    print(f"\n🛑 Shutting down gRPC server on port {port}...")
    await server.stop(grace=1)
    print("✅ Shutdown complete.")