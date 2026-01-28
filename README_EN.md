# Professional ETL Pipeline - 100% Windows Compatible

A professional-grade ETL (Extract, Transform, Load) pipeline for data processing and transformation, built with Python and best practices in data engineering. **Fully compatible with Windows, Linux, and macOS.**

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/pandas-2.1.3-blue.svg)](https://pandas.pydata.org/)
[![Pytest](https://img.shields.io/badge/pytest-7.4.3-blue.svg)](https://docs.pytest.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)

---

## 🌟 Overview

This project implements a robust and professional ETL pipeline that allows you to:

- **Extract** data from multiple formats (CSV, JSON, Excel, Parquet)
- **Transform** data with complex and chained operations
- **Load** results in different formats
- **Validate** data at each stage
- **Log** all operations with advanced logging
- **Monitor** performance with detailed statistics

## ✨ Key Features

| Category | Feature | Description |
|---|---|---|
| **Extraction** | Multiple Format Support | CSV, JSON, Excel, Parquet |
| | Auto-Detection | Identifies file type by extension |
| | Encoding Support | UTF-8 and Latin-1 for CSV files |
| **Transformation** | 9 Operations | Duplicates, missing values, rename, select, filter, convert, normalize, calculated columns, aggregation |
| | Fluent API | Method chaining for readability |
| **Validation** | 7 Validation Types | Email, phone, numeric, date, string, list, schema |
| **Loading** | Multiple Formats | CSV, JSON, Excel, Parquet |
| **Operations** | Structured Logging | Complete operation tracking |
| | Detailed Statistics | Performance and processing metrics |
| | Environment Config | `.env` support for different environments |
| **Compatibility** | **100% Windows** | `.bat` scripts and Windows-optimized code |
| | Cross-Platform | Works on Windows, Linux, and macOS |

---

## 🚀 Getting Started - Step by Step for Beginners

### Prerequisites

- **Python 3.9 or higher** (download from https://www.python.org/downloads/)
- **Git** (optional, for cloning - download from https://git-scm.com/)

### Step 1: Download the Project

#### Option A: Using Git (Recommended for Beginners)

1. Open **Command Prompt (CMD)** or **PowerShell**
   - On Windows: Press `Win + R`, type `cmd`, and press Enter

2. Copy and paste this command:
   ```cmd
   git clone https://github.com/lucasandre16112000-png/03-etl-pipeline.git
   ```

3. Press Enter and wait for it to finish

4. Navigate to the project folder:
   ```cmd
   cd 03-etl-pipeline
   ```

#### Option B: Download ZIP

1. Go to: https://github.com/lucasandre16112000-png/03-etl-pipeline
2. Click the green "Code" button
3. Click "Download ZIP"
4. Extract the ZIP file to a folder on your computer
5. Open **Command Prompt (CMD)** and navigate to the extracted folder:
   ```cmd
   cd C:\path\to\03-etl-pipeline
   ```

### Step 2: Run the Setup Script

Now you're in the project folder. Simply run:

**On Windows (CMD or PowerShell):**
```cmd
run_example.bat
```

**On Linux/macOS (Terminal):**
```bash
chmod +x run_example.sh
./run_example.sh
```

That's it! The script will automatically:
- ✅ Create a virtual environment (`venv`)
- ✅ Install all dependencies
- ✅ Run the example pipeline
- ✅ Generate output files

### Step 3: Check the Results

After the script finishes, you'll find the processed data in:
```
data/output/
├── processed_data.csv      # Data in CSV format
├── processed_data.json     # Data in JSON format
├── processed_data.xlsx     # Data in Excel format
└── pipeline_stats.json     # Processing statistics
```

---

## 📖 How to Use

### Basic Example

Create a file called `my_pipeline.py`:

```python
from etl.pipeline import ETLPipeline

# Create pipeline
pipeline = ETLPipeline()
pipeline.run()

# Extract, transform, and load
pipeline.extract("data/input/my_data.csv") \
    .remove_duplicates() \
    .handle_missing_values(strategy="drop") \
    .load("data/output/result.csv")

pipeline.finish()
```

Run it with:
```cmd
python my_pipeline.py
```

### Advanced Example

```python
from etl.pipeline import ETLPipeline

pipeline = ETLPipeline()
pipeline.run()

pipeline.extract("data/input/customers.csv") \
    .remove_duplicates(subset=["email"]) \
    .handle_missing_values(strategy="fill", fill_value=0) \
    .rename_columns({"id": "customer_id", "name": "customer_name"}) \
    .filter_rows(lambda df: df["age"] > 18) \
    .convert_types({"age": "int", "salary": "float"}) \
    .add_column("age_group", lambda row: "Senior" if row["age"] >= 60 else "Adult") \
    .load("data/output/customers.csv") \
    .load("data/output/customers.json") \
    .load("data/output/customers.xlsx")

pipeline.finish(execution_time=5.2)
pipeline.save_stats("data/output/stats.json")
```

---

## 🧪 Running Tests

To verify everything is working correctly:

**On Windows:**
```cmd
run_tests.bat
```

**On Linux/macOS:**
```bash
chmod +x run_tests.sh
./run_tests.sh
```

All tests should pass ✅

---

## 📂 Project Structure

```
03-etl-pipeline/
├── venv/                          # Virtual environment (created automatically)
├── data/
│   ├── input/                     # Input data
│   └── output/                    # Processed data
├── logs/                          # Log files
├── etl/                           # Main code
│   ├── config/                    # Configuration
│   ├── extractors/                # Data extractors
│   ├── loaders/                   # Data loaders
│   ├── transformers/              # Data transformers
│   ├── validators/                # Data validators
│   ├── exceptions.py              # Custom exceptions
│   ├── pipeline.py                # Main pipeline
│   └── profiler.py                # Performance monitor
├── tests/                         # Tests
├── .env.example                   # Example environment variables
├── .gitignore
├── example_usage.py               # Example usage
├── requirements.txt               # Dependencies
├── run_example.bat                # Windows script
├── run_example.sh                 # Linux/Mac script
├── run_tests.bat                  # Windows test script
├── run_tests.sh                   # Linux/Mac test script
├── WINDOWS_SETUP.md               # Windows installation guide
└── README.md                      # Portuguese documentation
```

---

## 🔧 Configuration

Create a `.env` file in the project root (copy from `.env.example`) to customize:

```
LOG_LEVEL=INFO
BATCH_SIZE=1000
MAX_WORKERS=4
STRICT_MODE=False
REMOVE_DUPLICATES=True
HANDLE_MISSING_VALUES=True
```

---

## ❓ Troubleshooting

### "Python not found"
- Install Python from https://www.python.org/downloads/
- **IMPORTANT**: Check "Add Python to PATH" during installation
- Restart your computer

### "pip not found"
- Python is installed but not in PATH
- Restart your computer after installing Python
- Or use: `python -m pip install` instead of `pip install`

### "Module not found"
- Make sure you're in the project folder
- Make sure `venv` is activated (you should see `(venv)` in your terminal)
- Run: `pip install -r requirements.txt`

### Script won't run
- Make sure you're in the correct folder
- Try running as Administrator (right-click CMD → "Run as administrator")
- Check that all files were extracted properly

---

## 📚 More Information

For more detailed information, see:
- **Portuguese documentation**: `README.md`
- **Windows setup guide**: `WINDOWS_SETUP.md`
- **Example code**: `example_usage.py`

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the project
2. Create a branch for your feature
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📝 License

This project is under the MIT license. See the LICENSE file for details.

---

## 👨‍💻 Author

Lucas André S - [GitHub](https://github.com/lucasandre16112000-png)

**Enhanced and made 100% Windows compatible by Manus AI**

---

## 🎯 Quick Start Cheat Sheet

```bash
# 1. Download and enter project
git clone https://github.com/lucasandre16112000-png/03-etl-pipeline.git
cd 03-etl-pipeline

# 2. Run the example (Windows)
run_example.bat

# 2. Run the example (Linux/Mac)
chmod +x run_example.sh
./run_example.sh

# 3. Check results in data/output/

# 4. Run tests (Windows)
run_tests.bat

# 4. Run tests (Linux/Mac)
chmod +x run_tests.sh
./run_tests.sh
```

That's all you need! Enjoy! 🎉
