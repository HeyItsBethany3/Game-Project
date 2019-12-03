class ScoreManager:
    def __init__(self):
        open('records.txt', 'a')
        with open('records.txt', 'r+') as f:
            try:
                self.record = int(f.read())
            except:
                self.record = 0

    def get_records(self):
        return self.record

    def set_new_record(self, score):
        with open('records.txt', 'w') as f:
            f.write(str(score))
        self.record = score
