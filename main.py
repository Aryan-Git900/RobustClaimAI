import argparse
import sys


def main():
    parser = argparse.ArgumentParser(
        description="Run the robust insurance claim prediction project."
    )
    parser.add_argument(
        "command",
        choices=["virtual", "train", "generate", "download"],
        nargs="?",
        default="virtual",
        help="virtual: run the virtual CLI demo (default); train: train the model; generate: regenerate synthetic dataset; download: fetch real dataset from the web"
    )
    args = parser.parse_args()

    if args.command == "virtual":
        try:
            from ml.virtual_predict import main as virtual_main
        except ImportError:
            print("Error: could not import virtual demo. Make sure the project structure is intact.")
            sys.exit(1)
        virtual_main()
    elif args.command == "train":
        try:
            from ml.train_model import main as train_main
        except ImportError:
            print("Error: could not import training script. Make sure the project structure is intact.")
            sys.exit(1)
        train_main()
    elif args.command == "download":
        try:
            from ml.generate_data import download_insurance_data
            from pathlib import Path
        except ImportError:
            print("Error: could not import data downloader. Make sure the project structure is intact.")
            sys.exit(1)
        data_path = Path(__file__).resolve().parent / "insurance.csv"
        df = download_insurance_data(data_path)
        print(f"Downloaded {data_path} with {len(df)} samples.")
    elif args.command == "generate":
        try:
            from ml.generate_data import generate_insurance_data
            from pathlib import Path
        except ImportError:
            print("Error: could not import data generator. Make sure the project structure is intact.")
            sys.exit(1)
        data_path = Path(__file__).resolve().parent / "insurance.csv"
        df = generate_insurance_data(1338)
        df.to_csv(data_path, index=False)
        print(f"Generated {data_path} with {len(df)} samples.")


if __name__ == "__main__":
    main()
