# -*- coding: utf-8 -*-

import click
from runner_manager import RunnerManager


@click.command()
@click.argument('cfgfile')
@click.option('--driver', default='firefox',
			  help='selenium driver: firefox|chrome|phantomjs. Default: firefox')
@click.option('--driver-path', default='',
			  help='Selinium driver path. Default: tries to find in driver in system PATH')
def main(cfgfile, driver, driver_path):
    """
    Console script for voamos
    """
    click.echo('Driver: "{}"'.format(driver))
    click.echo('Driver path: "{}"'.format(driver_path))

    rm = RunnerManager(cfgfile, driver=driver, driver_path=driver_path)
    click.echo('Running conf "%s"' % cfgfile)
    rm.run_conf_set()


if __name__ == '__main__':
	main()