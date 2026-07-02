from pipeline.logger import get_logger


def main():

    logger = get_logger()

    logger.info("Pipeline started.")
    logger.warning("This is a warning.")
    logger.error("This is a test error.")

    print("Logger test complete.")


if __name__ == "__main__":
    main()