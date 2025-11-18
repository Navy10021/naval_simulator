# Naval Mine Warfare Simulator 🚢⚓
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

3D tactical mine field simulation and risk analysis for naval operations.

![Demo](docs/images/demo_results.png)

   
## Features

- ✅ 3D mine field deployment simulation
- ✅ Surface vessel and submarine path analysis
- ✅ Multiple route scenario comparison
- ✅ Tactical deployment strategies (linear + random)
- ✅ Comprehensive risk assessment dashboard

## Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run basic simulation
python src/main.py

# Results will be saved in ./output/
```

## Installation
```bash
git clone https://github.com/yourusername/Naval-Mine-Warfare-Simulator.git
cd Naval-Mine-Warfare-Simulator
pip install -r requirements.txt
```

## Usage

### Basic Simulation
```python
from src.simulation import TacticalMineSimulation
from src.config import TacticalMineConfig, ThreatLevel

# Create configuration
config = TacticalMineConfig(threat_level=ThreatLevel.HIGH)

# Run simulation
sim = TacticalMineSimulation(config)
results = sim.run_simulation(...)
```

### Route Scenarios
```python
# Compare different route strategies
scenarios = sim.run_scenario_comparison(
    sub_start=(1000, 1000, 100),
    sub_end=(9000, 9000, 200)
)
```

## Simulation Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| Area Size | Simulation area (m) | 10km × 10km |
| Max Depth | Maximum depth (m) | 280m |
| Threat Level | MODERATE / HIGH / CRITICAL | HIGH |
| Mine Count | Number of mines | 150 / 300 / 450 |

## Results

### Threat Level Comparison
- **MODERATE (150 mines)**: 50% target risk
- **HIGH (300 mines)**: 75% target risk
- **CRITICAL (450 mines)**: 90% target risk

### Route Scenarios
- Direct: Straight line path
- Zigzag: Evasive maneuvering
- Deep Dive: Deep water avoidance
- Coastal: Shallow water route

## Output Files

- `tactical_*.png`: Mine deployment visualizations
- `route_scenarios_*.png`: Route comparison charts
- `comparison_dashboard.png`: Comprehensive analysis
- `results_*.json`: Detailed statistics

## Project Structure
```
src/          - Source code
examples/     - Example scripts
docs/         - Documentation
tests/        - Unit tests
notebooks/    - Jupyter notebooks
output/       - Simulation results
```

## Requirements

- Python 3.8+
- NumPy
- Matplotlib
- SciPy

## License

MIT License

## Citation

If you use this simulator in your research, please cite:
```bibtex
@software{naval_mine_simulator_2025,
  author = {Your Name},
  title = {Naval Mine Warfare Simulator},
  year = {2025},
  url = {https://github.com/yourusername/Naval-Mine-Warfare-Simulator}
}
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Contact

- Author: NAVY LEE
- Email: iyunseob4@gmail.com

## Acknowledgments

- Developed for naval tactical analysis and research
- Inspired by modern mine warfare doctrine
