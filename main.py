from openai import OpenAI
import os
import dotenv
from time import sleep
from types import SimpleNamespace

dotenv.load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPEN_KEY")
)

def create_file(file_name):
    file = client.files.create(
        file=open(file_name, "rb"),
        purpose="assistants"
    )

    print("Created file with id: " + file.id)

    return file.id

def create_assistant_with_file(file_id):

    assistant = client.beta.assistants.create(
        model="gpt-3.5-turbo-1106",
        name="lion",
        instructions="You are a helpfull assistant. You should only answer based on the files found.",
        tools=[{"type": "retrieval"}],
        file_ids=[file_id]
    )

    print("Created assistant with id: " + assistant.id)
    return assistant

def create_thread_with_file(file_id):
    thread = client.beta.threads.create()
    print("Created thread with id: " + thread.id)
    return thread

def main():
    try:

        file_id = create_file("lions.txt")
        assistant = create_assistant_with_file(file_id)
        thread = create_thread_with_file(file_id)

        # thread = SimpleNamespace(id='thread_hz10PqiGhWlzzoVFCg2CXPfo')
        # assistant = SimpleNamespace(id='asst_eWhmdk0rTMSBcAPuqVjzzQRx') 

        persistant_usage = True

        while persistant_usage:

            question = input("Question: ")

            # create the message associated with the thread
            client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=question,
                # file_ids=[file.id]
            )
        
            # run thread

            run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=assistant.id,
                tools=[
                    {
                        "type": "retrieval"
                    }
                ],
                model="gpt-3.5-turbo-1106"
            )

            # keep track of the run status

            ran = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )

            while ran.status != "completed":
                sleep(2)
                ran = client.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id
                )

                if ran.status == "failed":
                    print("Failed")
                    break

                print(ran.status)

            # retrieve the all mesages from the thread

            messages = client.beta.threads.messages.list(
                thread_id=thread.id
            )

            print(messages)
            print('\n\n')
            print('\n\n')
            print('\n\n')


            arrayOfMessages = []

            # loop through object list messages.data
            for x in messages.data:
                print(x.content[0].text.value)
                print('\n\n')
                arrayOfMessages.append(x.content[0].text.value)

            print('\n\n')
            print('\n\n')
            print('\n\n')
            
            print(arrayOfMessages.reverse())

            question = input("Still ask?(y/n): ")

            if question == 'n':
                persistant_usage = False

        print("Done")
    except Exception as error:
        print(error)

main()
