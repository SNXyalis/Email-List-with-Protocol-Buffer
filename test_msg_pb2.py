import msg_pb2
from multipledispatch import dispatch
import sys

if len(sys.argv) != 2:
  print("Usage:", sys.argv[0], "ADDRESS_BOOK_FILE")
  sys.exit(-1)

mail_list = msg_pb2.mailList()

def read_object():
    try:
        f = open(sys.argv[1], "rb")
        mail_list.ParseFromString(f.read())
        f.close()
    except Exception as exceptionError:
        print(f'Error during read: {exceptionError}')

def test_read_object():
    print("\n\n--Read Test--")
    print("Preparing to read object from file")
    read_object()
    print(mail_list)
    print("--END OF Read Test--\n\n")
    
@dispatch(str, int, str)
def write_object(name, id, email):
    try:
        person = mail_list.people.add()
        person.name=name
        person.id=id
        person.email=email
        f = open(sys.argv[1], "wb")
        f.write(mail_list.SerializeToString())
        f.close()
    except Exception as exceptionError:
        print(f'Error during write: {exceptionError}')

@dispatch(msg_pb2.Person)
def write_object(obj):
    try:
        person = mail_list.people.add()
        person.name = obj.name
        person.id = obj.id
        person.email = obj.email
        f = open(sys.argv[1], "wb")
        f.write(mail_list.SerializeToString())
        f.close()
    except Exception as exceptionError:
        print(f'Error during write: {exceptionError}')


def test_write_object():
    print('\n\n--Write Test--')
    print('--Case 1--')

    print('Writing with id,name,email as arguments')
    write_object('Bob', 4, 'bob@example.dot')

    print('--Case 2--')

    print('Writing with object as argument')
    person=msg_pb2.Person()
    person.name="Alice"
    person.id=3
    person.email="alice@example.dot"
    write_object(person)
    
    print("--END of Write Test--\n\n")


if __name__ ==  "__main__":
    test_write_object()
    test_read_object()