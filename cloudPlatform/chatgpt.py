import os
import time

from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def query_gpt(prompt: str, model: str = "gpt-4"):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    if response.choices:
        return response.choices[0].message.content

    return None


def query_gpt_assistant(prompt: str, assistantId: str):
    thread = client.beta.threads.create()

    client.beta.threads.messages.create(
        thread_id=thread.id,
        content=prompt,
        role="user",
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistantId,
    )

    while True:
        run = client.beta.threads.runs.retrieve(run_id=run.id, thread_id=thread.id)
        if run.status in ("complete", "failed", "canceled"):
            break

        time.sleep(3)

    response = client.beta.threads.messages.list(
        run_id=run.id,
        thread_id=thread.id,
    )

    client.beta.threads.delete(thread_id=thread.id)

    if response.messages:
        return response.messages[0].content
    return None
