# QRApp Backend

## Project Setup

### Prerequisites

1. Install UV Package Manager:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Clone the repository:
```bash
git clone https://github.com/QRCoffee/QRApp-BackEnd.git
cd QRApp-BackEnd
```

3. Create environment file `.env`:
```ini
# MongoDB
ACCESS_KEY=
REFRESH_KEY=
MONGO_URL=
REDIS_URL=
```

### Development Setup

1. Create and activate virtual environment:
```bash
uv venv
source .venv/Scripts/activate # Windows
source .venv/bin/activate # Linux/MacOS
```
2. Install dependencies:
```bash
uv sync
```

3. Run 
```bash
make dev # Dev Mode
make production # Production Mode
```
