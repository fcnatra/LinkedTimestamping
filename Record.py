import hashlib
import datetime

class Record():
    def __init__(self, content: str, previous_hash: str = None):
        if not previous_hash:
            genesis = hashlib.sha3_256(b'0x0')
            previous_hash = genesis.hexdigest()
        
        self.__content = content
        self.__previous_hash = previous_hash
        self.__timestamp = datetime.datetime.now()
        self.__hash = self.__build(content, previous_hash, self.__timestamp)

    def __build(self, content: str, previous_hash: str, timestamp: datetime) -> hash:
        hash = hashlib.sha3_256(content.encode('utf-8'))
        hash.update(previous_hash.encode('utf-8' ))
        hash.update(timestamp.__str__().encode('utf-8'))
        return hash

    def get_hex_hash(self) -> str:
        return self.__hash.hexdigest()

    def get_content(self) -> str:
        return self.__content
    
    def get_previous_hash(self) -> str:
        return self.__previous_hash

    def get_timestamp(self) -> datetime:
        return self.__timestamp

    def verify(self) -> bool:
        original_hash = self.get_hex_hash()
        current_hash = self.__build(self.__content, self.__previous_hash, self.__timestamp).hexdigest()

        return original_hash == current_hash
    