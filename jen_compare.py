#!/usr/bin/env python
import click
import requests
from bs4 import BeautifulSoup


def get_set_from_html(html):
    """
    :param html: Parsed BS html
    :return: set of failing tests names
    """
    fail_table = html.find_all('table')[1]
    failed = set()
    for row in fail_table.find_all('tr')[1:]:
        failed.add(row.find_all('a')[2].text)

    return failed


@click.option('--base')  # e.g.: http://localhost:8000/job
@click.option('--main')  # e.g.: 'backport-main/20'
@click.option('--feature')  # e.g.: 'backport-branches/74'
@click.command()
def main(base, main, feature):
    main_branch = "{}/{}/testReport/".format(base, main)
    feature_branch = "{}/{}/testReport/".format(base, feature)
    click.echo("Comparing test results between {} and {}".format(main_branch, feature_branch))

    main_doc = BeautifulSoup(requests.get(main_branch).content, 'html.parser')
    feature_doc = BeautifulSoup(requests.get(feature_branch).content, 'html.parser')

    main_failed = get_set_from_html(main_doc)
    feature_failed = get_set_from_html(feature_doc)

    click.echo("Failed in the main branch: {}".format(len(main_failed)))
    click.echo("Failed in the feature branch: {}".format(len(feature_failed)))

    new_failed = sorted(feature_failed - main_failed)
    click.echo("\n === Failed in feature, green in main. Total: {} ===".format(len(new_failed)))
    for line in new_failed:
        click.echo(line)

    main_fixed = sorted(main_failed - feature_failed)
    click.echo("\n === Green in feature, failed in main. Total: {} ===".format(len(main_fixed)))
    for line in main_fixed:
        click.echo(line)


if __name__ == "__main__":
    main()
