import asyncio
import hashlib
import aiofiles
import os
import time
import bcrypt

HERE = os.path.dirname(os.path.abspath(__file__))
PW_LIST = f'{HERE}/../wordlists/ignis-10M.txt'

def md5_hash(password):
    return hashlib.md5(password.encode()).hexdigest()

def sha1_hash(password):
    return hashlib.sha1(password.encode()).hexdigest()

def sha256_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

def sha512_hash(password):
    return hashlib.sha512(password.encode()).hexdigest()

def bcrypt_hash(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

async def process_chunk(start, end, filename):
    try:
        async with aiofiles.open(filename, 'r', encoding='utf-8') as file:
            await file.seek(start)
            lines = await file.read(end - start)
            lines = lines.splitlines()
            lines = [line.strip() for line in lines]
            async with aiofiles.open(f'{HERE}/../data/hashes.txt', 'a', encoding='utf-8') as f:
                for password in lines:
                    line_text = f'{password},{md5_hash(password)},{sha1_hash(password)},{sha256_hash(password)},{sha512_hash(password)},{bcrypt_hash(password)}'
                    await f.write(line_text + '\n')
    except Exception as e:
        print(f"Error processing chunk: {e}")


def chunkify(filename, size=1024*1024*10):
    file_end = os.path.getsize(filename)
    with open(filename, 'rb') as file:
        chunk_end = file.tell()
        while True:
            chunk_start = chunk_end
            file.seek(size, 1)
            file.readline()
            chunk_end = file.tell()
            yield chunk_start, chunk_end
            if chunk_end >= file_end:
                break

async def main(filename):
    tasks = []
    for chunk_start, chunk_end in chunkify(filename):
        file_end = os.path.getsize(filename)
        print(f"Processing chunk: {chunk_start} - {chunk_end} of {file_end}")
        task = asyncio.create_task(process_chunk(chunk_start, chunk_end, filename))
        tasks.append(task)

    print(f"Processing {len(tasks)} chunks")
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    # save password and all hash
    start_time = time.time()
    asyncio.run(main(PW_LIST))
    end_time = time.time()
    print(f"Time elapsed in minutes: {(end_time - start_time) / 60}")
