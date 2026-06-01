import multiprocessing


def main() -> None:
    from sentinel_engine.server import run

    run()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
