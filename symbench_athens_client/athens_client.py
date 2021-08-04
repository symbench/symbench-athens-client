import jenkins

__all__ = ["SymbenchAthensClient"]


class SymbenchAthensClient:
    """The client to the symbench athens server.

    Parameters
    ----------
    jenkins_url: str
        The url for the jenkins server
    username: str
        The username to login with
    password: str
        The password to login with

    Attributes
    ----------
    server: jenkins.Jenkins
        The python interface for the jenkins server
    """

    def __init__(self, jenkins_url, username, password):
        self.server = jenkins.Jenkins(jenkins_url, username=username, password=password)

    def get_user_info(self):
        """Return information for the currently logged in user."""
        return self.server.get_whoami()

    def get_available_jobs(self, names_only=False):
        """Returns available jobs from the server.

        Parameters
        ----------
        names_only: bool, default=False
            If true, return the job names only

        Returns
        -------
        list of dict or list of str
            The jobs available in the server
        """
        jobs = self.server.get_all_jobs()
        return list(map(lambda x: x["fullname"], jobs)) if names_only else jobs

    def get_job_info(self, job_name):
        """Get information about the job and its builds"""
        self.server.assert_job_exists(job_name)
        return self.server.get_job_info(job_name)

    def get_job_config(self, job_name):
        """Get the jenkins configuration XML for the Job"""
        self.server.assert_job_exists(job_name)
        return self.server.get_job_config(job_name)

    def can_execute(self):
        """Return True if any worker nodes are connected"""
        executor_nodes = list(
            filter(lambda node: node["name"] != "master", self.server.get_nodes())
        )
        return not all(node["offline"] for node in executor_nodes)

    def run_job_and_wait(self, job_name, params):
        assert self.can_execute(), "None of the executor nodes are online/connected"
        build_number = self.server.build_job(job_name, parameters=params)
        return build_number

    def get_job_status(self, build_number):
        """Check the job status based on build number"""
        self.server.get_build_info(build_number)


if __name__ == "__main__":
    client = SymbenchAthensClient(
        jenkins_url="http://localhost:8080", username="symcps", password="symcps2021"
    )

    build_number = client.run_job_and_wait(
        "cloneDesign",
        {"FromDesignName": "QuadCopter", "ToDesignName": "QuadCopterCopy2"},
    )

    print(client.get_job_status(build_number))
