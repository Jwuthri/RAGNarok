import click


@click.group(help="Command Line Interface for various tasks.")
def cli():
    """
    This command line interface provides various utilities and tasks,
    grouped by functionality. For detailed help on each command, run
    the command with the --help option.
    """
    pass


# Add sub-command to the main CLI


if __name__ == "__main__":
    cli()
