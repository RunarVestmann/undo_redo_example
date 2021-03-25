from enum import Enum


class OperationType(Enum):
    ADD = 0
    REMOVE = 1


class Operation:
    def __init__(self, type, data):
        self.type = type
        self.data = data


class PersonList:
    def __init__(self):
        self.__undo_stack = []
        self.__redo_stack = []
        self.__array = []

    def add(self, person, allow_undo=True):
        self.__array.append(person)
        if allow_undo:
            self.__undo_stack.append(Operation(OperationType.ADD, person))

    def remove(self, person, allow_undo=True):
        if person not in self.__array:
            return
        self.__array.remove(person)
        if allow_undo:
            self.__undo_stack.append(Operation(OperationType.REMOVE, person))

    def undo(self):
        if len(self.__undo_stack) == 0:
            return
        operation = self.__undo_stack.pop()

        if operation.type == OperationType.ADD:
            self.remove(operation.data, False)
        elif operation.type == OperationType.REMOVE:
            self.add(operation.data, False)

        self.__redo_stack.append(operation)

    def redo(self):
        if len(self.__redo_stack) == 0:
            return
        operation = self.__redo_stack.pop()

        if operation.type == OperationType.ADD:
            self.add(operation.data)
        elif operation.type == OperationType.REMOVE:
            self.remove(operation.data)

    def __str__(self):
        return "\n".join([str(person) for person in self.__array])


class Person:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return f"ID: {self.id}, Name: {self.name}"


if __name__ == "__main__":
    person_list = PersonList()
    person_list.add(Person(1, "Nonni"))
    person_list.add(Person(2, "Eva"))
    person_list.undo()
    person_list.undo()
    person_list.redo()
    person_list.redo()

    print(person_list)
