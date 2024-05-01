import logging
from typing import Optional

import boto3
from cachetools.func import ttl_cache
from requests_aws4auth import AWS4Auth

logger = logging.getLogger(__name__)


class OpenSearchAWSAuthMiddleware:
    def __init__(self, sts_role: str):
        self._sts_role = sts_role

    def __call__(self, req):
        return self._get_middleware(self._sts_role)(req)

    @staticmethod
    @ttl_cache(ttl=3500, maxsize=1)
    def _get_middleware(sts_role):
        sts_client = boto3.client("sts")
        assumedRole = sts_client.assume_role(
            RoleArn=sts_role,
            RoleSessionName="RAG",
            DurationSeconds=3600,
        )
        credentials = assumedRole["Credentials"]
        session = boto3.session.Session(
            aws_access_key_id=credentials["AccessKeyId"],
            aws_secret_access_key=credentials["SecretAccessKey"],
            aws_session_token=credentials["SessionToken"],
        )

        credentials = session.get_credentials()
        logger.info("Initialize AWS authentication")
        return AWS4Auth(
            credentials.access_key,
            credentials.secret_key,
            "us-west-2",
            "es",
            session_token=credentials.token,
        )


def get_opensearch_aws_auth_middleware(
    sts_role: Optional[str],
) -> Optional[OpenSearchAWSAuthMiddleware]:
    """
    Get a middleware which can be used to authenticate with OpenSearch running on AWS
    Parameters
    ----------
    sts_role : Optional[str]
        The name of the STS role to assume. If None, no authentication is used
    Returns
    -------
    Optional[AWS4Auth]
        The authentication for OpenSearch running on AWS
    """

    if not sts_role:
        return None

    return OpenSearchAWSAuthMiddleware(sts_role)
