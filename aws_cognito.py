#!/usr/bin/env python3
import readline
import sys
import boto3
import json
import requests


help_message = """Usage: python3 aws_cognito.py [OPTION]

Options: 
    get\t\t Get User Attributes
    update\t Update User Attributes
        """


regions = [
    "eu-west-1",
    "eu-west-2",
    "eu-west-3",
    "eu-north-1",
    "eu-central-1",
    "us-east-1",
    "us-west-2",
    "us-west-1",
    "us-east-2",
    "sa-east-1",
    "me-south-1",
    "ca-central-1",
    "ap-southeast-1",
    "ap-southeast-2",
    "ap-south-1",
    "ap-northeast-1",
    "ap-northeast-2",
    "ap-east-1"
]

def region_selection(func, access_token, list_=None):
    for r in regions:
        print(f"Trying to validate the token against {repr(r).upper()}")

        if not list_:
            response = func(access_token, r)
        else:
            response = func(access_token, r, list_)
        print()

        if response:
            return response


def get_user_attr(access_token, region):
    try:
        client = boto3.client("cognito-idp", region_name=region)
        response = client.get_user(AccessToken=access_token)
        return response

    except Exception as e:

        # if wrong region name was given
        if e.fmt:
            sys.exit(e.args[0])

        elif e.response["Error"]["Message"] == "Access Token has expired":
            sys.exit("[-] Access token has expired.")

        elif e.response["Error"]["Message"] == "Invalid Access Token":
            print("[-] Invalid Access Token")

        elif e.response["Error"]["Message"] == "Service Unavailable" and e.response["ResponseMetadata"]["MaxAttemptsReached"] == True:
            print(f"Rate limit has reached for {region}. Try agian later.")

        else:
            print(e)


def update_user_attr(access_token, region, list_):
    try:
        client = boto3.client("cognito-idp", region_name=region)
        response = client.update_user_attributes(UserAttributes=list_, AccessToken=access_token)
        return response

    except Exception as e:

        # if wrong region name was given
        if e.fmt:
            sys.exit(e.args[0])

        elif e.response["Error"]["Message"] == "Access Token has expired":
            sys.exit("[-] Access token has expired.")

        elif e.response["Error"]["Message"] == "Invalid Access Token":
            print("[-] Invalid Access Token")

        elif e.response["Error"]["Message"] == "Service Unavailable" and e.response["ResponseMetadata"]["MaxAttemptsReached"] == True:
            print(f"Rate limit has reached for {region}. Try agian later.")

        else:
            print(e)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(help_message)
    print()


    if sys.argv[1] == 'get':
        # access_token = input('Welcome, Please Enter Access Token: ')
        access_token = input('Welcome, Please Enter \033[93m\033[1mAccess Token\033[00m: ')
        region = input('\nPlease Enter Region Name: (leave blank if region unknown) ')
        print()
            
        if region:
            response = get_user_attr(access_token, region)
        else:
            response = region_selection(get_user_attr, access_token)

        try:
            del response["ResponseMetadata"]
        except Exception as e:
            print(e)

        print(json.dumps(response, indent=2))
    

    if sys.argv[1] == 'update':
        access_token = input('Welcome, Please Enter Access Token: ')
        region = input('\nPlease Enter Region Name: (leave blank if region unknown) ')
        # print()

        list_ = []
        print("\nPlease enter attribute's name and value. Type 'q' to quit")
        while True:
            name = input("\nEnter Attribute Name: ")

            if name == "q":
                break
            value = input("Enter Attribute Value: ")
            list_.append({"Name": name, "Value": value})
            # update_user_attr(access_token, region, list_)
        
        if region:
            response = update_user_attr(access_token, region, list_)
        else:
            response = region_selection(update_user_attr, access_token, list_)


        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            print('Operation Succeeded. \nRun script again with "get" option to confirm.')
        else:
            print(json.dumps(response, indent=2))


    if sys.argv[1] not in ['get', 'update']:
        sys.exit(help_message)
