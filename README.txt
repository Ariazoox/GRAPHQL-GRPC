# GRAPHQL-GRPC Microservices Architecture

A microservices-based movie booking system demonstrating mixed API communication patterns using GraphQL, gRPC, and REST. This project showcases a distributed architecture where services communicate through different protocols based on their use cases.

## 🏗️ Architecture Overview

The system consists of four independent microservices:

- **Movie Service** (GraphQL) - Manages movie and actor data
- **Showtime Service** (gRPC) - Handles movie schedules and showtimes
- **Booking Service** (gRPC) - Manages user bookings with Showtime validation
- **User Service** (REST) - Handles user management and booking operations

### Service Communication Flow

```
User Service (REST)
    ├──> Booking Service (gRPC)
    │       └──> Showtime Service (gRPC)
    └──> Movie Service (GraphQL)
```

## 📦 Services

### 1. Movie Service (Port 3001)
- **Protocol**: GraphQL
- **Framework**: Flask + Ariadne
- **Features**:
  - Query movies by ID or title
  - Retrieve all movies
  - Update movie ratings
  - Create and delete movies
  - Fetch actors for movies
- **GraphQL Playground**: `http://localhost:3001/graphql`

### 2. Showtime Service (Port 3000)
- **Protocol**: gRPC
- **Features**:
  - Get all movie schedules and showtimes
  - Returns date-based movie listings

### 3. Booking Service (Port 3002)
- **Protocol**: gRPC (acts as both server and client)
- **Features**:
  - Get user bookings by user ID
  - Add new bookings for users
  - Validates bookings against Showtime service
- **gRPC Client**: Makes calls to Showtime service

### 4. User Service (Port 3203)
- **Protocol**: REST (acts as REST server, gRPC and GraphQL client)
- **Framework**: Flask
- **Features**:
  - Get user by ID
  - Get user bookings (fetches from Booking service via gRPC, enriches with Movie data via GraphQL)
  - Create bookings for users (validates through Booking service)
- **gRPC Client**: Communicates with Booking service
- **GraphQL Client**: Queries Movie service for movie details

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- pip
- (Optional) PyCharm 2023.1.3 or later
- (Optional) Postman for API testing

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Ariazoox/GRAPHQL-GRPC.git
   cd GRAPHQL-GRPC
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate gRPC Python files** (if needed)
   ```bash
   # For Booking service
   cd booking
   python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/booking.proto ./protos/showtime.proto
   
   # For Showtime service
   cd ../showtime
   python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/showtime.proto
   
   # For User service
   cd ../user
   python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/booking.proto
   ```

### Running the Services

Each service should be run independently in separate terminal windows:

1. **Start Showtime Service** (must be started first)
   ```bash
   cd showtime
   python showtime.py
   ```
   Output: `Server started` on port 3000

2. **Start Booking Service**
   ```bash
   cd booking
   python booking.py
   ```
   Output: `Server started` on port 3002

3. **Start Movie Service**
   ```bash
   cd movie
   python movie.py
   ```
   Output: `Server running on port 3001`

4. **Start User Service**
   ```bash
   cd user
   python user.py
   ```
   Output: `Server running on port 3203`

## 📝 API Usage Examples

### GraphQL (Movie Service)

**Query a movie by ID:**
```graphql
{
  movie_with_id(_id: "123") {
    id
    title
    director
    rating
    actors {
      id
      firstname
      lastname
    }
  }
}
```

**Update movie rating:**
```graphql
mutation {
  update_movie_rate(_id: "123", _rate: 8.5) {
    id
    title
    rating
  }
}
```

Access the GraphQL Playground at: `http://localhost:3001/graphql`

### REST (User Service)

**Get user by ID:**
```bash
GET http://localhost:3203/users/{userid}
```

**Get user bookings:**
```bash
GET http://localhost:3203/users/{userid}/bookings
```

**Create a booking:**
```bash
POST http://localhost:3203/users/{userid}/bookings
Content-Type: application/json

{
  "date": "20151130",
  "movieid": "123"
}
```

### gRPC Services

For testing gRPC services, you'll need to use a gRPC client or generate client code from the proto files.

**Example Python gRPC client for Booking service:**
```python
import grpc
import booking_pb2
import booking_pb2_grpc

with grpc.insecure_channel("localhost:3002") as channel:
    stub = booking_pb2_grpc.BookingStub(channel)
    booking = stub.GetUserBookings(booking_pb2.UserId(userid="user123"))
    print(booking)
```

## 📁 Project Structure

```
GRAPHQL-GRPC/
├── booking/              # Booking gRPC service
│   ├── booking.py        # Main service file
│   ├── booking_pb2.py    # Generated gRPC code
│   ├── booking_pb2_grpc.py
│   ├── showtime_pb2.py   # Showtime client stubs
│   ├── showtime_pb2_grpc.py
│   ├── protos/           # Protocol buffer definitions
│   ├── data/             # JSON data files
│   └── requirements.txt
├── movie/                # Movie GraphQL service
│   ├── movie.py          # Main service file
│   ├── movie.graphql     # GraphQL schema
│   ├── resolvers.py      # GraphQL resolvers
│   ├── data/             # JSON data files
│   └── requirements.txt
├── showtime/             # Showtime gRPC service
│   ├── showtime.py       # Main service file
│   ├── showtime_pb2.py   # Generated gRPC code
│   ├── showtime_pb2_grpc.py
│   ├── protos/           # Protocol buffer definitions
│   ├── data/             # JSON data files
│   └── requirements.txt
├── user/                 # User REST service
│   ├── user.py           # Main service file
│   ├── booking_pb2.py    # Booking client stubs
│   ├── booking_pb2_grpc.py
│   ├── protos/           # Protocol buffer definitions
│   ├── data/             # JSON data files
│   └── requirements.txt
└── requirements.txt      # Root dependencies
```

## 🔧 Technology Stack

- **Python 3**
- **Flask** - Web framework for REST and GraphQL services
- **Ariadne** - GraphQL library
- **gRPC** - High-performance RPC framework
- **Protocol Buffers** - Data serialization for gRPC
- **JSON** - Data storage format

## 🎯 Key Features

- ✅ Mixed API communication (GraphQL, gRPC, REST)
- ✅ Microservices architecture
- ✅ Inter-service communication patterns
- ✅ Service-to-service validation (Booking validates with Showtime)
- ✅ Data enrichment (User service enriches bookings with movie details)

## 📄 License

See [LICENSE](LICENSE) file for details.

## 🤝 Contributing

This is an educational project demonstrating microservices architecture with mixed API protocols.

## 📧 Contact

For questions or issues, please open an issue on the repository.
