---
hide:
  - navigation
---
# Getting Started

## Introduction

Quantcast CLI, accessible via the `ctop` command, is designed to analyze cookie log files and identify the most active cookie on a specified date. It processes files containing cookie IDs along with their corresponding timestamps, and outputs the most frequently encountered cookie ID for a given day.

## Installation

To install Quantcast CLI, use pip by running the following command in your terminal:

```bash
pip install quantcast_cli
```

Make sure Python and pip are installed on your system before executing the above command.

## Usage

The `ctop` command requires a log file in CSV format with each record comprising a cookie ID and a timestamp. It accepts the following main arguments:

- `-f` or `--file`: Specifies the path to the cookie log file. The default value is `cookie_log.csv`.
- `-d` or `--date`: Sets the target date for which to find the most active cookie, formatted as `YYYY-MM-DD`. The default date is `2018-12-09`.

### Command Syntax

```plaintext
 Usage: ctop [OPTIONS]

╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────╮
│ --file                -f      PATH        Cookies file path [default: cookie_log.csv]             │
│ --date                -d      [%Y-%m-%d]  Targeted date in UTC format [default: 2018-12-09]       │
│ --install-completion                      Install completion for the current shell.               │
│ --show-completion                         Show completion for the current shell.                  │
│ --help                                    Show this message and exit.                             │
╰───────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### Example

To find the most active cookie on December 9, 2018, from a file named `cookie_log.csv`, use:

```bash
ctop -f cookie_log.csv -d 2018-12-09
```

This command outputs the cookie ID(s) with the highest number of occurrences on the specified date to stdout.

### Options

- `--install-completion`: Installs shell completion for the current shell.
- `--show-completion`: Displays the completion setup script for the current shell, allowing you to copy or customize its installation.
- `--help`: Shows the help message, detailing all available options.

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

