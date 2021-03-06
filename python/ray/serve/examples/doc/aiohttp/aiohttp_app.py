# File name: aiohttp_app.py
from aiohttp import web

import ray
from ray import serve

# Connect to the running Ray cluster.
ray.init(address="auto")

# Fetch the ServeHandle to query our model.
my_handle = serve.get_deployment("my_model").get_handle()


# Define our AIOHTTP request handler.
async def handle_request(request):
    # Offload the computation to our Ray Serve deployment.
    result = await my_handle.remote("dummy input")
    return web.Response(text=result)


# Set up an HTTP endpoint.
app = web.Application()
app.add_routes([web.get("/dummy-model", handle_request)])

if __name__ == "__main__":
    web.run_app(app)
