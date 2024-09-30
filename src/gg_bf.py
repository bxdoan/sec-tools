import asyncio
import json, time
import os

import aiofiles

HERE = os.path.dirname(os.path.abspath(__file__))

async def read_list_json(file_path):
    async with aiofiles.open(file_path, mode='r') as f:
        return json.loads(await f.read())

async def find_password_in_file(info, pw, file_hash, output_file):
    async with aiofiles.open(file_hash, mode='r') as file, aiofiles.open(output_file, mode='a') as out_file:
        if not pw:
            return False
        async for l in file:
            if pw in l:
                print(f"Found password {info},{pw}")
                await out_file.write(f"{info},{l}\n")
                return True
        return False

async def process_account(accounts, file_data):
    file_hash = f'{HERE}/../../../Documents/hashes.txt'
    file_res_path = f'{HERE}/res.txt'
    print(f"Processing {file_data} with {len(accounts)} accounts")
    for idx, acc in enumerate(accounts):
        info = acc.get('nricfin') or acc.get('email') or acc.get('mobile')
        pw = acc.get('password')
        print (f"{file_data} | {idx+1}/{len(accounts)} | {acc['id']} : info={info} | PW {pw}")
        await find_password_in_file(info, pw, file_hash, file_res_path)

async def main():
    st = time.time()
    tasks = []
    for j in range(25):
        file_data = f'{HERE}/gg/{j + 1}.txt'
        accounts = await read_list_json(file_data)
        task = asyncio.create_task(process_account(accounts,f'{j + 1}.txt'))
        tasks.append(task)

    await asyncio.gather(*tasks)
    print(f"Processing {len(tasks)} files")
    print(f"Time taken: {time.time() - st}")


if __name__ == '__main__':
    asyncio.run(main())