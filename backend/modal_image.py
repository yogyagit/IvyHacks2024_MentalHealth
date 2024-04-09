from modal import Image, Stub, Secret

image = Image.debian_slim(python_version="3.11").pip_install(
    "modal==0.62.21",
     "nomic",
     "cohere",
     "fastapi",
     ).apt_install("git", "curl")

stub = Stub(
    name="ThinkWell",
    image=image,
    secrets=[Secret.from_name("nomic-key")],
)