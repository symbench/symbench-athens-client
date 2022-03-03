from symbench_athens_client.athens_jenkins_client import SymbenchAthensJenkinsClient

if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        "url", type=str, metavar="JENKINS_URL", help="The URL of the jenkins server"
    )
    parser.add_argument(
        "username",
        type=str,
        metavar="JENKINS_USERNAME",
        help="The username to login with",
    )
    parser.add_argument(
        "password",
        type=str,
        metavar="JENKINS_PASSWORD",
        help="The password to login with",
    )

    args = parser.parse_args()
    athens_client = SymbenchAthensJenkinsClient(
        jenkins_url=args.url, username=args.username, password=args.password
    )
