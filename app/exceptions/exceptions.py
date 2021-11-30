class InvalidCategoryError(Exception):
    ...

class UniqueViolation(Exception):
    ...

class InvalidImportanceOrUrgencyError(Exception):
    def __init__(self, urgency, importance):
        super().__init__(urgency, importance)
        self.message = {"error": {
            "valid_options": {
                "importance": [1,2],
                "urgency": [1,2]
            },
            "received_options": {
                "importance": importance,
                "urgency": urgency
            }
        }}

class UniqueTaskError(Exception):
    ...

class UpdateImportanceOrUrgencyError(Exception):
    ...