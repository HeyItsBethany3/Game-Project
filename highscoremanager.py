class ScoreManager:
    def __init__(self):
        open('records.txt', 'a')   # Opens file for appending
        with open('records.txt', 'r+') as f:
            try:
                self.record = int(f.read())
                # .read() extracts all characters in file as string
            except: # Do we need type of error?
                self.record = 0

    def get_records(self):
        return self.record

    def set_new_record(self, score):
        with open('records.txt', 'w') as f: # write to file 
            f.write(str(score))
        self.record = score
        
    # Do you ever have to close the file?
    # Replaces what's in file
