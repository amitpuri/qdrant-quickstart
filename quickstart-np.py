import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import CollectionStatus, Distance, VectorParams, PointStruct
import uuid
import random
import os

# Global variables
client = None
my_collection = "qdrant_101_collection"
data = None
point_ids = None
query_vector = None

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the main header"""
    print("🚀 Qdrant 101 - Interactive Tutorial")
    print("=" * 50)

def connect_to_qdrant():
    """Connect to Qdrant instance"""
    global client
    try:
        client = QdrantClient("http://localhost:6333")
        print("✅ Connected to Qdrant at http://localhost:6333")
        return True
    except Exception as e:
        print(f"❌ Failed to connect to Qdrant: {e}")
        return False

def show_main_menu():
    """Display the main menu"""
    print("\n📋 Main Menu:")
    print("1.  Setup Collection & Data")
    print("2.  Collection Information")
    print("3.  Insert/Update Points")
    print("4.  Retrieve Points")
    print("5.  Vector Search")
    print("6.  Filtered Search")
    print("7.  Batch Search")
    print("8.  Scroll Collection")
    print("9.  Delete Points")
    print("10. Advanced Payload Operations")
    print("11. Run All Operations (Demo Mode)")
    print("12. Reset Collection")
    print("0.  Exit")
    print("-" * 30)

def setup_collection_and_data():
    """Setup collection and generate sample data"""
    global data, point_ids, query_vector
    
    print("\n1️⃣ Setting up Collection & Data")
    print("-" * 30)
    
    # Check if collection exists
    if client.collection_exists(collection_name=my_collection):
        collection_info = client.get_collection(collection_name=my_collection)
        if collection_info.points_count > 0:
            print(f"📊 Collection '{my_collection}' already exists with {collection_info.points_count} points.")
            choice = input("🔄 Recreate collection? (y/n): ").lower()
            if choice == 'y':
                client.delete_collection(collection_name=my_collection)
                print("🗑️ Collection deleted")
                # Create new collection after deletion
                try:
                    first_collection = client.create_collection(
                        collection_name=my_collection,
                        vectors_config=VectorParams(size=100, distance=Distance.COSINE)
                    )
                    print(f"✅ Collection '{my_collection}' created successfully")
                    print(f"   Vector size: 100")
                    print(f"   Distance metric: COSINE")
                except Exception as e:
                    print(f"❌ Failed to create collection: {e}")
                    return False
            else:
                print("📁 Using existing collection")
                # Don't return here - continue to data generation
        else:
            print(f"📁 Collection '{my_collection}' exists but is empty. Using existing collection.")
            # Don't return here - continue to data generation
    else:
        # Create collection only if it doesn't exist
        try:
            first_collection = client.create_collection(
                collection_name=my_collection,
                vectors_config=VectorParams(size=100, distance=Distance.COSINE)
            )
            print(f"✅ Collection '{my_collection}' created successfully")
            print(f"   Vector size: 100")
            print(f"   Distance metric: COSINE")
        except Exception as e:
            print(f"❌ Failed to create collection: {e}")
            return False
    
    # Generate sample data
    num_points = input("📊 Number of points to generate (default 1000): ").strip()
    num_points = int(num_points) if num_points.isdigit() else 1000
    
    data = np.random.uniform(low=-1.0, high=1.0, size=(num_points, 100))
    point_ids = list(range(len(data)))
    query_vector = np.random.uniform(low=-1.0, high=1.0, size=100).tolist()
    
    print(f"✅ Generated {len(data)} random vectors of dimension {data.shape[1]}")
    print(f"   Data type: {type(data[0, 0])}")
    print(f"   Sample values: {data[0, :5].tolist()}")
    print(f"✅ Created point IDs: {point_ids[:5]}...{point_ids[-5:]}")
    print(f"✅ Generated query vector: {query_vector[:5]}")
    
    return True

def show_collection_info():
    """Display collection information"""
    print("\n4️⃣ Collection Information")
    print("-" * 30)
    
    try:
        collection_info = client.get_collection(collection_name=my_collection)
        print(f"📊 Collection Status: {collection_info.status}")
        print(f"📊 Points Count: {collection_info.points_count}")
        print(f"📊 Vector Size: {collection_info.config.params.vectors.size}")
        print(f"📊 Distance Metric: {collection_info.config.params.vectors.distance}")
    except Exception as e:
        print(f"❌ Failed to get collection info: {e}")

def insert_points():
    """Insert points into collection"""
    print("\n3️⃣ Inserting Points")
    print("-" * 30)
    
    if data is None:
        print("❌ No data available. Please run 'Setup Collection & Data' first.")
        return
    
    try:
        upsert_result = client.upsert(
            collection_name=my_collection,
            points=models.Batch(
                ids=point_ids,
                vectors=data.tolist()
            )
        )
        print(f"✅ Successfully inserted {len(point_ids)} points")
        print(f"   Operation ID: {upsert_result.operation_id}")
    except Exception as e:
        print(f"❌ Failed to insert points: {e}")

def retrieve_points():
    """Retrieve specific points"""
    print("\n4️⃣ Retrieving Points")
    print("-" * 30)
    
    ids_input = input("🔍 Enter point IDs to retrieve (comma-separated, e.g., 0,100,500): ").strip()
    if not ids_input:
        ids_input = "0,100,500,999"
    
    try:
        retrieve_ids = [int(x.strip()) for x in ids_input.split(',')]
        retrieved_points = client.retrieve(
            collection_name=my_collection,
            ids=retrieve_ids,
            with_vectors=True
        )
        print(f"✅ Retrieved {len(retrieved_points)} points by ID")
        for point in retrieved_points:
            print(f"   Point ID: {point.id}, Vector (first 5): {point.vector[:5]}")
    except Exception as e:
        print(f"❌ Failed to retrieve points: {e}")

def vector_search():
    """Perform vector similarity search"""
    print("\n5️⃣ Vector Search")
    print("-" * 30)
    
    if query_vector is None:
        print("❌ No query vector available. Please run 'Setup Collection & Data' first.")
        return
    
    limit = input("🔍 Number of results to return (default 5): ").strip()
    limit = int(limit) if limit.isdigit() else 5
    
    try:
        search_response = client.query_points(
            collection_name=my_collection,
            query=query_vector,
            limit=limit,
            with_vectors=True
        )
        print(f"🔍 Query vector (first 5): {query_vector[:5]}")
        print(f"✅ Found {len(search_response.points)} similar vectors:")
        for i, result in enumerate(search_response.points):
            print(f"   Rank {i+1}: ID={result.id}, Score={result.score:.4f}, Vector (first 3): {result.vector[:3]}")
    except Exception as e:
        print(f"❌ Failed to perform vector search: {e}")

def filtered_search():
    """Perform filtered search"""
    print("\n6️⃣ Filtered Search")
    print("-" * 30)
    
    if query_vector is None:
        print("❌ No query vector available. Please run 'Setup Collection & Data' first.")
        return
    
    print("🔍 Filter Options:")
    print("1. Filter by point IDs (using retrieve)")
    print("2. Filter by payload field")
    print("3. Filter by range values")
    
    filter_choice = input("Select filter type (1-3, default 1): ").strip()
    if not filter_choice:
        filter_choice = "1"
    
    try:
        if filter_choice == "1":
            # Filter by point IDs using retrieve
            filter_ids = input("🔍 Enter point IDs to filter by (comma-separated, default: 0,100,200,300,400): ").strip()
            if not filter_ids:
                filter_ids = "0,100,200,300,400"
            
            filter_id_list = [int(x.strip()) for x in filter_ids.split(',')]
            print(f"📋 Retrieving points with IDs: {filter_id_list}")
            
            # Use retrieve to get specific points, then show them
            retrieved_points = client.retrieve(
                collection_name=my_collection,
                ids=filter_id_list,
                with_vectors=True
            )
            print(f"✅ Found {len(retrieved_points)} points with specified IDs:")
            for i, point in enumerate(retrieved_points):
                print(f"   Point {i+1}: ID={point.id}, Vector (first 3): {point.vector[:3]}")
                
        elif filter_choice == "2":
            # Filter by payload field (requires payload data)
            print("💡 This requires points with payload data. Creating sample payload points first...")
            
            # Create some points with payload
            payload_points = []
            for i in range(5):
                payload_points.append(PointStruct(
                    id=2000 + i,
                    vector=np.random.uniform(low=-1.0, high=1.0, size=100).tolist(),
                    payload={
                        "category": random.choice(["red", "blue", "green"]),
                        "value": random.randint(1, 100),
                        "active": random.choice([True, False])
                    }
                ))
            
            # Insert payload points
            client.upsert(collection_name=my_collection, points=payload_points)
            print(f"✅ Inserted {len(payload_points)} points with payload")
            
            # Now search with payload filter
            category = input("🔍 Enter category to filter by (red/blue/green, default: red): ").strip()
            if not category:
                category = "red"
            
            payload_response = client.query_points(
                collection_name=my_collection,
                query=query_vector,
                query_filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="category",
                            match=models.MatchValue(value=category)
                        )
                    ]
                ),
                limit=5,
                with_payload=True
            )
            print(f"✅ Found {len(payload_response.points)} points with category '{category}':")
            for i, result in enumerate(payload_response.points):
                print(f"   Rank {i+1}: ID={result.id}, Score={result.score:.4f}, Payload: {result.payload}")
                
        elif filter_choice == "3":
            # Filter by range values
            min_value = input("🔍 Enter minimum value (default: 50): ").strip()
            min_value = int(min_value) if min_value.isdigit() else 50
            
            max_value = input("🔍 Enter maximum value (default: 80): ").strip()
            max_value = int(max_value) if max_value.isdigit() else 80
            
            print(f"💡 Creating points with value range {min_value}-{max_value}...")
            
            # Create points with range values
            range_points = []
            for i in range(5):
                range_points.append(PointStruct(
                    id=3000 + i,
                    vector=np.random.uniform(low=-1.0, high=1.0, size=100).tolist(),
                    payload={
                        "value": random.randint(min_value, max_value),
                        "type": f"range_{i}"
                    }
                ))
            
            # Insert range points
            client.upsert(collection_name=my_collection, points=range_points)
            print(f"✅ Inserted {len(range_points)} points with value range")
            
            # Search with range filter
            range_response = client.query_points(
                collection_name=my_collection,
                query=query_vector,
                query_filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="value",
                            range=models.Range(gte=min_value, lte=max_value)
                        )
                    ]
                ),
                limit=5,
                with_payload=True
            )
            print(f"✅ Found {len(range_response.points)} points with value in range {min_value}-{max_value}:")
            for i, result in enumerate(range_response.points):
                print(f"   Rank {i+1}: ID={result.id}, Score={result.score:.4f}, Value: {result.payload.get('value', 'N/A')}")
        else:
            print("❌ Invalid filter choice")
            
    except Exception as e:
        print(f"❌ Failed to perform filtered search: {e}")

def batch_search():
    """Perform batch search"""
    print("\n7️⃣ Batch Search")
    print("-" * 30)
    
    num_queries = input("🔍 Number of query vectors (default 2): ").strip()
    num_queries = int(num_queries) if num_queries.isdigit() else 2
    
    try:
        query_vectors = [
            np.random.uniform(low=-1.0, high=1.0, size=100).tolist()
            for _ in range(num_queries)
        ]
        
        batch_results = client.query_batch_points(
            collection_name=my_collection,
            requests=[
                models.QueryRequest(query=qv, limit=3) for qv in query_vectors
            ]
        )
        print(f"✅ Batch search completed for {len(query_vectors)} queries")
        for i, response in enumerate(batch_results):
            print(f"   Query {i+1}: Found {len(response.points)} results")
            for j, result in enumerate(response.points):
                print(f"     Rank {j+1}: ID={result.id}, Score={result.score:.4f}")
    except Exception as e:
        print(f"❌ Failed to perform batch search: {e}")

def scroll_collection():
    """Scroll through collection"""
    print("\n8️⃣ Scroll Collection")
    print("-" * 30)
    
    limit = input("📜 Number of points to scroll (default 5): ").strip()
    limit = int(limit) if limit.isdigit() else 5
    
    try:
        scroll_results = client.scroll(
            collection_name=my_collection,
            limit=limit,
            with_vectors=True
        )
        print(f"✅ Scrolled through collection, found {len(scroll_results[0])} points")
        for point in scroll_results[0]:
            print(f"   Point ID: {point.id}, Vector (first 3): {point.vector[:3]}")
    except Exception as e:
        print(f"❌ Failed to scroll collection: {e}")

def delete_points():
    """Delete specific points"""
    print("\n9️⃣ Delete Points")
    print("-" * 30)
    
    delete_ids_input = input("🗑️ Enter point IDs to delete (comma-separated): ").strip()
    if not delete_ids_input:
        print("❌ No IDs provided")
        return
    
    try:
        delete_ids = [int(x.strip()) for x in delete_ids_input.split(',')]
        delete_result = client.delete(
            collection_name=my_collection,
            points_selector=models.PointIdsList(points=delete_ids)
        )
        print(f"✅ Deleted {len(delete_ids)} points: {delete_ids}")
        print(f"   Operation ID: {delete_result.operation_id}")
    except Exception as e:
        print(f"❌ Failed to delete points: {e}")

def payload_operations():
    """Advanced payload operations"""
    print("\n🔟 Advanced Payload Operations")
    print("-" * 30)
    
    num_payload_points = input("📦 Number of payload points to create (default 10): ").strip()
    num_payload_points = int(num_payload_points) if num_payload_points.isdigit() else 10
    
    try:
        # Create points with payload
        payload_points = []
        for i in range(num_payload_points):
            payload_points.append(PointStruct(
                id=1000 + i,
                vector=np.random.uniform(low=-1.0, high=1.0, size=100).tolist(),
                payload={
                    "category": random.choice(["A", "B", "C"]),
                    "value": random.randint(1, 100),
                    "description": f"Point {1000 + i}"
                }
            ))
        
        # Insert points with payload
        payload_upsert = client.upsert(
            collection_name=my_collection,
            points=payload_points
        )
        print(f"✅ Inserted {len(payload_points)} points with payload")
        
        # Search with payload filter
        if query_vector:
            payload_response = client.query_points(
                collection_name=my_collection,
                query=query_vector,
                query_filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="category",
                            match=models.MatchValue(value="A")
                        )
                    ]
                ),
                limit=3,
                with_payload=True
            )
            print(f"✅ Found {len(payload_response.points)} points with category 'A':")
            for result in payload_response.points:
                print(f"   ID: {result.id}, Score: {result.score:.4f}, Payload: {result.payload}")
    except Exception as e:
        print(f"❌ Failed to perform payload operations: {e}")

def run_all_operations():
    """Run all operations in demo mode"""
    print("\n🎬 Running All Operations (Demo Mode)")
    print("=" * 50)
    
    # Setup
    if not setup_collection_and_data():
        return
    
    # Insert data
    insert_points()
    
    # Show info
    show_collection_info()
    
    # Retrieve
    retrieve_points()
    
    # Search
    vector_search()
    filtered_search()
    batch_search()
    
    # Scroll
    scroll_collection()
    
    # Payload operations
    payload_operations()
    
    print("\n🎉 Demo Complete!")
    input("Press Enter to continue...")

def reset_collection():
    """Reset the collection"""
    print("\n🔄 Reset Collection")
    print("-" * 30)
    
    try:
        if client.collection_exists(collection_name=my_collection):
            client.delete_collection(collection_name=my_collection)
            print("✅ Collection deleted successfully")
        else:
            print("ℹ️ Collection doesn't exist")
        
        # Reset global variables
        global data, point_ids, query_vector
        data = None
        point_ids = None
        query_vector = None
        print("✅ Global variables reset")
    except Exception as e:
        print(f"❌ Failed to reset collection: {e}")

def main():
    """Main interactive loop"""
    clear_screen()
    print_header()
    
    # Connect to Qdrant
    if not connect_to_qdrant():
        print("❌ Cannot connect to Qdrant. Please ensure it's running on localhost:6333")
        return
    
    while True:
        show_main_menu()
        choice = input("🎯 Select an option (0-12): ").strip()
        
        if choice == '0':
            print("\n👋 Goodbye!")
            break
        elif choice == '1':
            setup_collection_and_data()
        elif choice == '2':
            show_collection_info()
        elif choice == '3':
            insert_points()
        elif choice == '4':
            retrieve_points()
        elif choice == '5':
            vector_search()
        elif choice == '6':
            filtered_search()
        elif choice == '7':
            batch_search()
        elif choice == '8':
            scroll_collection()
        elif choice == '9':
            delete_points()
        elif choice == '10':
            payload_operations()
        elif choice == '11':
            run_all_operations()
        elif choice == '12':
            reset_collection()
        else:
            print("❌ Invalid option. Please try again.")
        
        input("\nPress Enter to continue...")
        clear_screen()
        print_header()

if __name__ == "__main__":
    main()