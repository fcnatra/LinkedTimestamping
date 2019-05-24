from Record import Record

class LinkedTimestampChain():
    def __init__(self):
        self.__chain = []
        self.__error = None

    def get_chain(self) -> []:
        return self.__chain

    def add_content(self, content: str):
        if not content or len(content) == 0:
            raise Exception('content must not be empty')
        
        last_hash = None
        if len(self.__chain) > 0:
            last_hash = self.__chain[-1].get_hex_hash()
        
        record = Record(content, last_hash)
        self.__chain.append(record)
    
    def add_records(self, records: []):
        self.__chain += records

    def get_error(self) -> str:
        return self.__error
    
    def verify(self) -> bool:
        self.__error = None

        last_index = len(self.__chain)-1

        for index, record in enumerate(self.__chain):
            if not self.__verify_record(record):
                break

            if index != last_index and not self.__verify_linking(record, self.__chain[index+1]):
                break

        return self.__error is None

    def __verify_record(self, record):
        if not record.verify():
            self.__error = f'The content of the record at {record.get_timestamp()} has changed'
            return False
        
        return True

    def __verify_linking(self, record, next_record) -> bool:
        if record.get_hex_hash() != next_record.get_previous_hash():
            self.__error = f'Chain has changed between the records at {record.get_timestamp()} and {next_record.get_timestamp()}'
            return False

        return True

