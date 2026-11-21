from pathlib import Path

from tabulens.sample_data import write_sample

if __name__ == "__main__":
    print(write_sample(Path("data/campus_energy_sample.csv")))
