#!/usr/bin/env python3

""" Create a droplet on DigitalOcean using their v2 API """

import json
import sys
import requests

import click

def send_action(url, headers, package):
    """ Send request to DigitalOcean"""
    try:
        resp = requests.post(url, headers=headers, data=package)
        return resp
    except requests.exceptions.RequestException as err:
        print(err)
        sys.exit(1)

def do_create(endpoint, headers, name, image, region, size):
    """ Create request to send to DigitalOcean """
    url = endpoint+'droplets'

    package = {
        'name':name,
        'region':region,
        'size':size,
        'image':image}

    resp = send_action(url, headers, json.dumps(package))
    return resp

@click.command()
@click.option(
    '--token',
    default=None,
    required=True,
    help='DigitalOcean personal access token')
@click.option(
    '--name',
    default='no-imagination.used',
    help='Droplet name')
@click.option(
    '--image',
    default='ubuntu-14-04-x64',
    help='Operating system image to spin up')
@click.option(
    '--size',
    default='s-1vcpu-1gb',
    help='Droplet size slug')
@click.option(
    '--region',
    default='sfo2',
    help='DigitalOcean region to use')
def run(token, name, image, region, size):
    """ Main program """
    endpoint = 'https://api.digitalocean.com/v2/'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {tok}'.format(tok=token)}

    resp = do_create(endpoint, headers, name, image, region, size)

    # expecting a 202 accepted from DO if operation successful
    if resp.status_code == 202:
        data = resp.json()
        print('Droplet successfully created:')
        for key, value in data['droplet'].items():
            print('{k}: {v}'.format(k=key, v=value))
    else:
        print('There was an issue with creating the droplet. Received ',
              'HTTP status code {status}, expected a 202.'.format(
                  status=resp.status_code))
        print(resp.text)


if __name__ == '__main__':
    run()
