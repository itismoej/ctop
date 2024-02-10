---
hide:
  - navigation
---
# Getting Started

## Introduction

Quantcast CLI, accessible via the `ctop` command, is designed to analyze cookie log files and identify the most active cookie on a specified date. It processes files containing cookie IDs along with their corresponding timestamps, and outputs the most frequently encountered cookie ID for a given day.

## Installation

To install Quantcast CLI, use pip by running the following command in your terminal:

<!-- termynal -->

```console
$ pip install quantcast_cli
---> 100%
installed
```


Make sure Python and pip are installed on your system before executing the above command.

## Usage

The `ctop` command requires a log file in CSV format with each record comprising a cookie ID and a timestamp. It accepts the following main arguments:

- `-f` or `--file`: Specifies the path to the cookie log file. The default value is `cookie_log.csv`.
- `-d` or `--date`: Sets the target date for which to find the most active cookie, formatted as `YYYY-MM-DD`. The default date is `2018-12-09`.

### Command Syntax


<!-- termynal -->

```console
$ ctop --help

 Usage: ctop [OPTIONS]

╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────╮
│ --file                -f      PATH          Cookies file path [default: cookie_log.csv]             │
│ --date                -d      [%Y-%m-%d]    Targeted date in UTC format [default: 2018-12-09]       │
│ --install-completion                        Install completion for the current shell.               │
│ --show-completion                           Show completion for the current shell.                  │
│ --help                                      Show this message and exit.                             │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯
```


### Example

To find the most active cookie on December 9, 2018, from a file named `cookie_log.csv`, use:

<!-- termynal -->

```console
$ ctop -f cookie_log.csv -d 2018-12-09
AtY0laUfhglK3lC7
```

This command outputs the cookie ID(s) with the highest number of occurrences on the specified date to stdout.

### Options

- `--install-completion`: Installs shell completion for the current shell.
- `--show-completion`: Displays the completion setup script for the current shell, allowing you to copy or customize its installation.
- `--help`: Shows the help message, detailing all available options.

## Running with Docker

For users who prefer Docker or wish to run the Quantcast CLI tool in a containerized environment, we have provided a Docker image. This method simplifies the execution process and ensures compatibility across different environments.

### Prerequisites

- Docker must be installed on your system. For installation instructions, refer to the [official Docker documentation](https://docs.docker.com/get-docker/).

### Usage

To run the Quantcast CLI tool using Docker, you can use the following command structure:

<!-- termynal -->

```console
$ docker run -it --rm -v /cookie_log.csv:/file.csv \
    itismoej/ctop -f /file.csv -d YYYY-MM-DD
some-cookie-key
```

Replace `/cookie_log.csv` with the full path to your cookie log file on your host machine, `/file.csv` with the path and file name you want to use inside the container, and `YYYY-MM-DD` with the target date you're interested in.

### Example

If you have a cookie log file named `cookie_log.csv` located in `/home` on your machine, and you want to find the most active cookie for **December 9, 2018**, the command would look like this:

<!-- termynal -->

```console
$ docker run -it --rm -v /home/cookie_log.csv:/cookie_log.csv \
    itismoej/ctop -f /cookie_log.csv -d 2018-12-09
AtY0laUfhglK3lC7
```

This command mounts the `cookie_log.csv` file from your host into the Docker container and executes the ctop command inside the container to process the file. The `-it` flag is used to run the container interactively, and `--rm` ensures that the container is removed after execution to prevent accumulation of unused containers.

### Notes

- Ensure that the volume mapping (`-v` flag) correctly reflects the path to your cookie log file on your host and the desired path within the container.
- The Docker image `itismoej/ctop` is the official image for running the Quantcast CLI tool. Make sure to pull the latest version if you haven't done so recently.

Using Docker to run the Quantcast CLI tool provides a seamless and environment-independent way to analyze your cookie log files, eliminating the need for local Python environment setup.


## File Format

Your cookie log file must adhere to the following structure:

```csv
cookie,timestamp
```

Here, each line should contain a cookie ID, followed by its timestamp in the ISO 8601 format (`YYYY-MM-DDTHH:MM:SS+00:00`), separated by a comma and **sorted by timestamps in reverse order.**

### Sample Log File

```plaintext
cookie,timestamp
AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00
SAZuXPGUrfbcn5UA,2018-12-09T10:13:00+00:00
...
```

## Performance

The Quantcast CLI tool is optimized for high performance, capable of processing extensive datasets with efficiency. Below are the key performance optimizations that enable the tool to handle millions of records swiftly:

### Multi-processing with MapReduce

Quantcast CLI employs a multi-processing strategy, enhanced by the MapReduce programming model, to leverage the computing power of modern multi-core processors effectively. This approach allows the tool to parallelize the data processing workload across multiple cores, significantly reducing the overall processing time. The MapReduce model splits the processing task into two main phases: the Map phase, where the dataset is divided into smaller chunks that are processed in parallel, and the Reduce phase, where the results of these parallel processes are combined into a final output. This method is particularly effective for analyzing extensive log files, enabling the tool to process 8 million records in just 5 seconds on a computer with 4 CPU cores.

### Binary Search on Sorted Timestamps

The tool assumes that timestamps in the cookie log file are sorted. This assumption allows for the use of a binary search algorithm when filtering records by the specified date. This efficiency gain is crucial when dealing with large datasets, as it minimizes the time required to locate and filter records by date.


## Licence
This project is licensed under the terms of the MIT license.

