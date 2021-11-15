#!/usr/bin/env python
"""
Performs basic cleaning on the data and save the results in Weights & Biases
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(artifact_local_path)
    logger.info("Input dataframe read into memory with shape %s", df.shape)

    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()

    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])

    logging.info("Creating output artifact...")
    df.to_csv("clean_sample.csv", index=False)

    ######################
    # YOUR CODE HERE     #
    ######################
    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This step cleans the data")


    parser.add_argument(
        "--input_artifact", 
        type=str,  ## INSERT TYPE HERE: str, float or int
        help="Input artifact",  ## INSERT DESCRIPTION HERE
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,  ## INSERT TYPE HERE: str, float or int,
        help="Output artifact",  ## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,  ## INSERT TYPE HERE: str, float or int,
        help="Output type",  ## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,  ## INSERT TYPE HERE: str, float or int
        help="Output description",  ## INSERT DESCRIPTION HERE
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,  ## INSERT TYPE HERE: str, float or int,
        help="Minimum price",  ## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,  ## INSERT TYPE HERE: str, float or int,
        help="Maximum price",  ## INSERT DESCRIPTION HERE,
        required=True
    )

    args = parser.parse_args()

    go(args)
