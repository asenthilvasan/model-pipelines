import asyncio
import grpc

async def run_grpc_server(servicer_cls, add_servicer_fn, port: int, shutdown_event=None):
    server = grpc.aio.server()
    add_servicer_fn(servicer_cls(), server)
    server.add_insecure_port(f"[::]:{port}")

    await server.start()
    print(f"✅ gRPC server running on [::]:{port}")

    try:
        if shutdown_event:
            await shutdown_event.wait()
        else:
            await server.wait_for_termination()
    except asyncio.CancelledError:
        print("⚠️ Server cancelled, shutting down...")
    finally:
        await server.stop(grace=2)
        print("🛑 Server shut down.")