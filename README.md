# Qdrant Quickstart

A comprehensive quickstart guide and interactive tutorial for getting started with Qdrant vector database.

## 🚀 What is Qdrant?

Qdrant is a vector similarity search engine and vector database. It provides a production-ready service with a convenient API to store, search, and manage points (vectors) with an additional payload. Qdrant is tailored to extended filtering support, making it useful for all sorts of neural-network or semantic-based matching, faceted search, and other applications.

## 📁 Project Structure

This project contains two main Python scripts:

- **`quickstart.py`** - A simple, straightforward example showing basic Qdrant operations
- **`quickstart-np.py`** - An interactive, comprehensive tutorial with advanced features

## 🛠️ Prerequisites

Before running the examples, make sure you have:

1. **Python 3.7+** installed
2. **Qdrant server** running locally on `http://localhost:6333`

### Installing Qdrant

#### Option 1: Using Docker (Recommended)
```bash
docker run -p 6333:6333 qdrant/qdrant
```

#### Option 2: Using Docker Compose
```yaml
version: '3.8'
services:
  qdrant:
    image: qdrant/qdrant
    ports:
      - "6333:6333"
    volumes:
      - ./qdrant_storage:/qdrant/storage
```

#### Option 3: From Source
Follow the [official installation guide](https://qdrant.tech/documentation/quick-start/#installation).

## 📦 Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd qdrant-quickstart
```

2. Install the required Python packages:
```bash
pip install qdrant-client numpy
```

## 🎯 Quick Start

### Simple Example (`quickstart.py`)

Run the basic example to get familiar with Qdrant:

```bash
python quickstart.py
```

This script demonstrates:
- Connecting to Qdrant
- Creating a collection
- Basic collection operations

### Interactive Tutorial (`quickstart-np.py`)

For a comprehensive, hands-on experience:

```bash
python quickstart-np.py
```

This interactive tutorial includes:

#### 🎮 Menu Options:
1. **Setup Collection & Data** - Create collections and generate sample data
2. **Collection Information** - View collection details and statistics
3. **Insert/Update Points** - Add vectors to your collection
4. **Retrieve Points** - Get specific points by ID
5. **Vector Search** - Perform similarity search
6. **Filtered Search** - Search with filters and conditions
7. **Batch Search** - Search multiple vectors at once
8. **Scroll Collection** - Browse through collection data
9. **Delete Points** - Remove specific points
10. **Advanced Payload Operations** - Work with metadata and payloads
11. **Run All Operations** - Demo mode with all features
12. **Reset Collection** - Clean up and start fresh

## 🔧 Key Features Demonstrated

### Vector Operations
- **Collection Management**: Create, delete, and manage collections
- **Vector Insertion**: Add vectors with optional payload data
- **Similarity Search**: Find similar vectors using various distance metrics
- **Batch Operations**: Efficient bulk operations

### Advanced Features
- **Filtering**: Search with complex filters on payload data
- **Payload Management**: Store and query metadata alongside vectors
- **Distance Metrics**: Support for COSINE, EUCLIDEAN, and DOT product distances
- **Batch Processing**: Handle multiple queries efficiently

### Data Types Supported
- **Vectors**: High-dimensional numerical vectors
- **Payloads**: JSON-like metadata (strings, numbers, booleans, arrays)
- **Filters**: Complex query conditions on payload fields

## 📊 Example Data

The tutorial generates sample data including:
- Random vectors (100-dimensional by default)
- Point IDs for identification
- Query vectors for similarity search
- Payload data with categories, values, and descriptions

## 🎨 Interactive Features

The interactive tutorial (`quickstart-np.py`) provides:
- **User-friendly menus** with clear options
- **Input validation** and error handling
- **Progress feedback** with emojis and status messages
- **Flexible parameters** - customize vector dimensions, point counts, etc.
- **Demo mode** - run all operations automatically

## 🔍 Common Use Cases

This quickstart is perfect for:
- **Learning Qdrant basics** - Understanding core concepts
- **Prototyping** - Quick setup for vector search applications
- **Testing** - Validating Qdrant functionality
- **Development** - Building vector-based applications

## 📚 Next Steps

After completing the quickstart:

1. **Explore the Qdrant Documentation**: [https://qdrant.tech/documentation/](https://qdrant.tech/documentation/)
2. **Try Real Data**: Replace random vectors with your actual embeddings
3. **Build Applications**: Use Qdrant in your machine learning projects
4. **Advanced Features**: Explore clustering, recommendations, and more

## 🐛 Troubleshooting

### Connection Issues
- Ensure Qdrant is running on `localhost:6333`
- Check firewall settings
- Verify Docker container is accessible

### Performance Tips
- Use batch operations for large datasets
- Optimize vector dimensions for your use case
- Consider payload indexing for filtered searches

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve this quickstart guide.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🔗 Useful Links

- [Qdrant Official Website](https://qdrant.tech/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Qdrant GitHub](https://github.com/qdrant/qdrant)
- [Python Client Documentation](https://qdrant.github.io/qdrant-client/)

---

**Happy vector searching! 🎉**
