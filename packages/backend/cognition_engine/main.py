import os
import argparse
from core.file_watcher import start_file_watcher
from core.self_learning import train_initial_model

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sovereign Cognition Engine")
    parser.add_argument("--train", action="store_true", help="Train the initial model")
    parser.add_argument("--watch", type=str, help="Watch a directory", default="workspace")

    args = parser.parse_args()

    # Create necessary directories if they don't exist
    if not os.path.exists('models'):
        os.makedirs('models')
    if not os.path.exists('data'):
        os.makedirs('data')
    if not os.path.exists(args.watch):
        os.makedirs(args.watch)

    if args.train:
        train_initial_model()
    else:
        start_file_watcher(args.watch)
