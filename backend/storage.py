import requests
""" 
this file serves as storage for NFT media files on IPFS
questions on workflow: 
1. user upload image 
2. get the image in the backend, store in database?
3. upload to ipfs (done)
4. store the URI in database, along with minting
"""


nft_storage_url = "https://api.nft.storage/upload"
api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweDVjMjlFYjYxMjQ1OUM3YTIxNUJCNjY0MDQwNDMzNDk4QzAzN0ZCMDYiLCJpc3MiOiJuZnQtc3RvcmFnZSIsImlhdCI6MTYzNzY4OTE3NjMxNywibmFtZSI6InhycCB0ZXN0IGtleSJ9.HvzCF4V52Tse0Hp-EGL7eC6pZEcEEFG60HA9Z_1K2yM"

image_file = './static/nft_1.png'
image_file2 = "./static/nft_2.jpeg"
image_file3 = "./static/nft_3.png"
data = open(image_file3, 'rb').read()

# cid + ".ipfs.dweb.link" is the URI 
Headers = {"Authorization": f"Bearer {api_key}"}
response = requests.post(url=nft_storage_url, data=data, headers=Headers)
print(response.json()['value']['cid']+".ipfs.dweb.link")
