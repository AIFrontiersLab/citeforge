# Citeforge

Generate a verified, multi-source research brief from a single complex query.

# Research MVP

A minimal research synthesis tool.

## Usage

```bash
pip install -r requirements.txt
python -m main
```

## Demo

```bash
python -c "from main import demo; demo()"
```

## Tests

```bash
pytest tests/test_main.py -v
```

## Architecture

![Architecture](docs/architecture.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart LR
    A[User Query] --> B[Decompose Query]
    B --> C[Sub-queries]
    C --> D[Match Mock Data]
    D --> E[Synthesize Results]
    E --> F[Research Brief]
```

</details>
