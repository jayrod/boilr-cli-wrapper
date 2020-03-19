# -*- coding: utf-8 -*-

"""{{AppName}}.{{AppName}}: provides entry point main()."""

__version__ = "{{Version}}"

import argparse
import re
import sys
from glob import iglob
from ipaddress import ip_address
from json import dumps, loads
from json.decoder import JSONDecodeError
from os import environ
from pathlib import Path
from shutil import which
from subprocess import CompletedProcess, run
from typing import Tuple

from inquirer import Confirm, prompt
from markdown_table import Table
from tabulate import tabulate

from {{AppName}}.Util import Util


def insert_md_table(markdown: str, md_table: str) -> None:
    """ Inserts a markdown table into a document at a given tag placement.

        Arguments:
            markdown(str): Path to markdown file
            md_table(str): Markdown table text to be inserted

    """
    content = open(markdown, "r").read(-1)

    # regex
    regex = r"\[\[\s?{{NoteTag}}\s?\]\]"

    # if there exists a tag then substitute our data into it
    if re.findall(regex, content):
        content = re.sub(regex, md_table, content)
    else:
        content += md_table

    with open(markdown, "a") as m_file:
        m_file.write(content)

def run_binary({{binary}}_bin: str, options: dict) -> CompletedProcess:
    """ Runs the {{binary}} command with given options.

        Arguments:
            {{binary}}_bin(str): Path string to {{binary}}
            options(dict): dictionary containing options needed for running

        Returns:
            CompletedProcess: Output from {{binary}}
    """
    cmd = list()
    cmd.extend([{{binary}}_bin])
    cmd.extend([])

    output = run(cmd, capture_output=True)

    return output

def validate_input(args) -> ip_address:
    """ Validates and formulates user input. This function can make default
    decisions about where to get environment variable input from and what form
    it should take.

        Arguments:
            args(argparser): Arguments to validate

        Return:
            ip_address: Default target ip address

    """
    # determine if the input IP address is inface an IP
    ip = None

    try:
        # if no target host given
        if not args.target:
            # look for RHOST environ var
            if "RHOST" in environ.keys():
                print(msg("Using Environment variable for IP address"))
                ip = ip_address(environ["RHOST"])
        else:
            ip = ip_address(args.target)

    except ValueError:
        print(Util().err_msg("Argument or environment variable was not a valid IP address"))
        sys.exit()

    return ip

def info_to_table(rows: list) -> Tuple[list, list]:
    """ Formats raw row data into a table format that will be used
    with other render functions. This function is where column headers
    should be defined.

        Arguments:
            rows(list): Rows of data

        Return:
            List : List of column names
            List : Full table representation of data
    """
    columns = ["col1", "col2", "col3"]
    full_table = []

    for row in rows:
        # create table
        full_table.append([row["col1"], row["col2"], row["col3"]])

    return columns, full_table

def parse(cmd_output: str) -> list:
    """ Parse command output for suitable viewing 

        Arguments:
            cmd_output(str): Command output

        Returns:
            list: List of data containing dicts
    """
    regex = r"regex"
    matches = re.findall(regex, cmd_output)
    ret_list = [{"user": m[0], "rid": m[1]} for m in matches if m]

    return ret_list

def add_json_file(json_files: list, json_file: str) -> None:
    """ Adds a json file to a list structure. Performing sanity
    checks as well as converting the text to json objects

        Arguments:
            json_files(list): Mutable list to add json objects to
            json_file(str): Path to json file to read

    """
    try:
        json_files.append(loads(open(json_file, "r").read(-1)))
    except FileNotFoundError:
        print(Util().err_msg("File path is not valid"))
    except JSONDecodeError:
        print(Util().err_msg("File {0} was not valid json".format(json_file)))


def process_json_output(args):
    """ Processes json output from {{binary}} output


    """
    # holds all files to be processed
    json_files = list()

    if args.json_file:
        print(msg("Parsing json file {0}".format(args.json_file)))
        add_json_file(json_files, args.json_file)
    else:
        search_path = str(Path(curdir).joinpath("**/{{binary}}/*"))
        output_files = [f for f in iglob(search_path, recursive=True)]
        [add_json_file(json_files, output_file) for output_file in output_files]



def render_tab_table(columns: list, full_table: list) -> str:
    return tabulate(full_table, headers=columns, tablefmt="fancy_grid")

def render_md_table(columns: list, full_table: list) -> str:
    return Table(columns, full_table).render()

def render_text_info(data: list) -> str:
    output_string = ""

    for item in data:
        output_string += "SOMEVALUE : {0}\n".format("host")

    return output_string


def main():
    print("Executing {{AppName}} version %s." % __version__)

    parser = argparse.ArgumentParser(description="{{AppDescription}}")
    parser.add_argument("--target", help="IP address for target.")
    parser.add_argument("--markdown", help="Markdown File to append data.")
    parser.add_argument("--json", help="JSON file to write data.")
    parser.add_argument("--text", help="Text File to append data.")
    args = parser.parse_args()

    ip = validate_input(args)

    if not ip:
        print(Util().err_msg("Check IP argument"))
        sys.exit(-1)

    Util().append_scan_log("{{AppName}}")

    {{binary}}_bin = which("{{binary}}")
    if not {{binary}}_bin:
        print(Util().err_msg("Unable to locate {{binary}} binary"))
        sys.exit(1)

    print(Util().msg("Located {{binary}} binary : {0}".format({{binary}}_bin)))

    cmd_output = run_binary({{binary}}_bin, str(ip))
    if cmd_output.returncode:
        print(Util().err_msg("{{binary}} returned with an error code"))
        print("Error : {0}\nOutput : {1}".format(cmd_output.stderr, cmd_output.stdout))
        sys.exit(1)

    print(Util().msg("Parsing Output returned from {{binary}}"))
    output = parse(str(cmd_output.stdout))

    if not output:
        print(Util().err_msg("Was unable to parse information from {{binary}} output"))
        sys.exit(1)

    # create column and output data
    columns, table = info_to_table(output)

    # if Output file given then write output to it
    if args.markdown:
        print(Util().msg("Writing markdown to file"))
        md_table = render_md_table(columns, table)
        insert_md_table(args.markdown, md_table)

    # if json argument given then write to file
    if args.json:
        
        # if folder doesn't exist then create it
        if not Path(args.json).parent.exists():
            Path(args.json).parent.mkdir(parents=True)

        print(Util().msg("Writing json to file"))
        with open(args.json, "w") as json_file:
            json_file.write(dumps(output, indent=4))
    
    # if text argument given then output to text file
    if args.text:
        print(Util().msg("Writing scan results to text file"))
        text = render_text_info(data_dict)

        # if folder doesn't exist then create it
        if not Path(args.text).parent.exists():
            Path(args.text).parent.mkdir(parents=True)

        with open(args.text, "a") as text_file:
            text_file.write("\n")
            text_file.write(text)
        
    print(Util().msg("Results"))
    tabulate_table = render_tab_table(columns, table)

    print(tabulate_table)
