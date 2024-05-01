import threading
from collections import namedtuple

from rag.utilities.logging_tools import get_logger

logger = get_logger(__name__)
obj_key = namedtuple("obj_key", ["tenantId", "botId", "context", "search_idx"])


def synchronized(func_):
    """A decorator imposing synchronized access to functions and methods"""
    lock = threading.Lock()

    def inner(*args, **kwargs):
        with lock:
            return func_(*args, **kwargs)

    return inner


class ObjectStore:
    """
    Maintains a shared dict keyed by (tenant, bot, context) and values tuples of
        class object and lock objects (mutexes).
        The shared dict is managed by get and reset methods of the object.

        Each of these methods is thread-safe for a given (tenant, bot, context) key i.e
        multiple simultaneous requests to read or change the contents of the dictionary are serialized
    """

    _dicts = {}

    def __init__(self, Class2Call) -> None:
        self.Class2Call = Class2Call

    @property
    def sharedMemory(self):
        """
        An instance property providing read access to _dicts shared memory
        """
        return self._dicts

    @synchronized
    def getWriteLock(self, okey: obj_key):
        return ObjectStore._dicts.setdefault(okey, (None, threading.Lock()))[1]

    def create(self, *args, **kwargs):
        return self.Class2Call(*args, **kwargs)

    def get(self, okey: obj_key, *args, **kwargs):
        """A wrapper providing safe access to KeyStore._dicts by kgnerKeyT"""

        # NB! threading.Lock class does not allow variable assignment in its contect-manager protocol implementation
        # i.e. 'with threading.Lock() as lck' does not work
        # We workaround this using Py3.8 implicit assignment operator
        with (wlck := self.getWriteLock(okey)):
            # When a lock is requested through getWriteLock, ObjectStore._dicts[okey] is created with service = None
            # In that case we create the service
            if any(x is None for x in ObjectStore._dicts[okey][:1]) is True:
                logger.info(
                    f"[KeyStore.get] (aisera_{okey.tenantId}, {okey.botId}, {okey.search_idx}) not in ObjectStore."
                )
                logger.debug(
                    f"Entered KeyStore.get({okey.tenantId}, {okey.botId} , {okey.search_idx})"
                )
                ObjectStore._dicts[okey] = (self.create(okey, *args, **kwargs), wlck)
                logger.debug(f"Left KeyStore.reset({okey.tenantId}, {okey.botId})")
            return ObjectStore._dicts[okey][0]

    def reset(self, okey: obj_key):
        """
        Read updated DB info into new Class2Call
        """
        with (wlck := self.getWriteLock(okey)):
            logger.info(
                f"[KeyStore.reset] Loading (aisera_{okey.tenantId}, {okey.botId}) from DB"
            )
            logger.debug(f"Entered KeyStore.reset({okey.tenantId}, {okey.botId})")
            service = self.create(okey)
            ObjectStore._dicts[okey] = (service, wlck)
            logger.debug(f"Left ObjectStore.reset({okey.tenantId}, {okey.botId})")

    def delete(self, okey: obj_key):
        """
        A thread-safe method to use with partition manager API
        NB! 2 threads can reach the 'with' statement simultaneously. The first will acquire the lock
        and remove okey. The reference to the lock held by the 2nd thread is still valid. The 2nd thread
        will safely pop an non-existing key and return.
        """
        if okey not in self._dicts:
            logger.warning(f"[ObjectStore.delete] {okey} not in KeyStore. Exiting")
            return

        with ObjectStore._dicts[okey][3]:
            logger.info(
                "[KeyStore.delete] Removing the value of ({tenant}, {botId})  from KeyStore.sharedMemory".format(
                    tenant=f"aisera_{okey.tenantId}", botId=okey.botId
                )
            )
            logger.debug(
                f"Entered ObjectStore.delete({okey.tenantId}, {okey.botId}, {okey.domain})"
            )
            _ = ObjectStore._dicts.pop(okey, None)
            logger.debug(
                f"Left ObjectStore.delete({obj_key.tenantId}, {obj_key.botId}, {obj_key.domain})"
            )

    def service_key(self, tenantId, botId, search_idx, context="local"):
        return obj_key(tenantId, botId, context, search_idx)
