from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import CollectionStatus

client = QdrantClient("http://localhost:6333") # Connect to existing Qdrant instance

my_collection = "first_collection"

# Check if collection exists and delete it if it does
if client.collection_exists(collection_name=my_collection):
    client.delete_collection(collection_name=my_collection)

# Create the collection
first_collection = client.create_collection(
    collection_name=my_collection,
    vectors_config=models.VectorParams(size=100, distance=models.Distance.COSINE)
)
print("Collection created:", first_collection)

# Read back the collection information
collection_info = client.get_collection(collection_name=my_collection)
print(collection_info)
print("\nCollection info:")
print(f"Name: {my_collection}")
print(f"Vector size: {collection_info.config.params.vectors.size}")
print(f"Distance metric: {collection_info.config.params.vectors.distance}")
print(f"Status: {collection_info.status}")
print(f"Points count: {collection_info.points_count}")

