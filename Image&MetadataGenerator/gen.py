from PIL import Image
import PIL
import random
import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import os

import time

fp = "./Layers"

ClothesFp = "/Clothes/"
BckFp = "/Background/"
BdyFp = "/Body/"
EyesFp = "/Eyes/"
MouthFp = "/Mouths/"
HeadwareFp = "/Hats/"
EarwareFp = "/Earwear/"
NecklacesFp = "/Neckalces/"
SunglassesFp = "/Sunglasses/"


EarwareTags = [
    "Cross",
    "Diamonds",
    "Gold Hoops",
    "Golden Studs",
    "Industrial",
    "Silver Hoops",
    "Silver Stud",
    "Stretchers",
    "Eye Patch",
]
ClothesTags = [
    "Basketball Vest",
    "Bow Tie",
    "Golden Jacket",
    "Hawian Shirt",
    "Honey on Body",
    "King Robe",
    "Leather Jacket",
    "Pimp Coat",
    "Plain T-Shirt",
    "Polo Shirt",
    "Polo Vest",
    "Ripped Shirt",
    "Scarf",
    "Shirt and Tie",
    "Smoking Jacket",
    "Space Suit",
    "Toga",
    "Tuxedo",
]
HeadwareTags = [
    "Bandana",
    "Baseball Hat",
    "Beanie",
    "Cowboy Hat",
    "Crown",
    "Dreads Hair",
    "Fez Hat",
    "Flat Hat",
    "Green Hair",
    "Honey on Top",
    "Horns",
    "Party Hat",
    "Rock Hair",
    "Sailor Hat",
    "Spinner Hat",
]
MouthTags = [
    "Big Growl",
    "Closed",
    "Gold Teeth",
    "Honey on Branch",
    "Knife in Mouth",
    "O-Shaped",
    "Party Horn in Mouth",
    "Pipe in Mouth",
    "Roar",
    "Side Grin",
    "Smile",
    "Snake Around Throat",
    "Tongue out",
]
EyesTags = [
    "Angry",
    "Closed",
    "Green Laser",
    "Open",
    "Red Laser",
    "Stoned",
    "Surprised",
    "Swirl",
    "Tired",
]
BackgroundTags = [
    "Tie-dye",
    "Bright Purple",
    "Brown",
    "Dark Blue",
    "Dark Green",
    "Dark Purple",
    "Gold",
    "Green",
    "Mint",
    "Pink",
    "Purple",
    "Red",
    "Silver",
]
BodyTags = [
    "Blue",
    "Bright Green",
    "Green",
    "Grey",
    "Mint",
    "Orange",
    "Pink",
    "Purple",
    "Red",
    "Yellow",
]
NecklaceTags = [
    "Bitcoin",
    "Diamond",
    "Frankenstien Bolts",
    "Golden",
    "Green Stone",
    "Red Stone",
    "Silver",
]
SunglassesTags = ["Black", "Yellow", "Red"]

counter = 1

pinataUrl = "https://api.pinata.cloud/pinning/pinFileToIPFS"


def uploadToIpfs(imageToUpload=None, jsonMetadata=None):
    if imageToUpload and jsonMetadata:
        print("You can only upload one at a time")
        return
    if imageToUpload:
        fileName = "image"

        m = MultipartEncoder(fields={"file": (fileName, open(imageToUpload, "rb"))})
    elif jsonMetadata:
        m = MultipartEncoder(
            fields={"file": ("jsonMetadata", json.dumps(jsonMetadata).encode("utf-8"))}
        )
    else:
        print("Not supported")
        return

    headers_to_use = {
        "pinata_api_key": "5539d2f63d608cd6d58a",
        "pinata_secret_api_key": "f31d77e37679d817c19abb13ace31825c602d577a37346a5807f92b16845be79",
        "Content-Type": m.content_type,
    }

    r = requests.post(pinataUrl, data=m, headers=headers_to_use)

    if r.status_code == 200:
        return r.json()["IpfsHash"]

    print(r.text)
    return None


def dataUpload(count):
    fpToUse = f"./generatedImages/Bear #{count}.png"
    return uploadToIpfs(imageToUpload=fpToUse)


while counter <= 10000:
    sunglasses = False

    bckId = random.randint(0, len(BackgroundTags) - 1)
    bodyId = random.randint(0, len(BodyTags) - 1)
    headwareId = random.randint(0, len(HeadwareTags) - 1)
    eyesId = random.randint(0, len(EyesTags) - 1)
    earsId = random.randint(0, len(EarwareTags) - 1)
    clothesId = random.randint(0, len(ClothesTags) - 1)
    mouthId = random.randint(0, len(MouthTags) - 1)
    necklaceId = random.randint(0, len(NecklaceTags) - 1)

    if random.randint(0, 100) <= 5:
        sunglassesId = random.randint(0, len(SunglassesTags) - 1)
        sunglasses = True
        while eyesId == 2 or eyesId == 4:
            eyesId = random.randint(0, len(EyesTags) - 1)
        while earsId == 8:
            earsId = random.randint(0, len(EarwareTags) - 1)

    back = Image.open(fp + BckFp + str(bckId) + ".png")
    body = Image.open(fp + BdyFp + str(bodyId) + ".png")
    ears = Image.open(fp + EarwareFp + str(earsId) + ".png")
    headware = Image.open(fp + HeadwareFp + str(headwareId) + ".png")
    eyes = Image.open(fp + EyesFp + str(eyesId) + ".png")
    mouth = Image.open(fp + MouthFp + str(mouthId) + ".png")
    clothes = Image.open(fp + ClothesFp + str(clothesId) + ".png")

    necklace = Image.open(fp + NecklacesFp + str(necklaceId) + ".png")
    if sunglasses:
        sunglasses = Image.open(fp + SunglassesFp + str(sunglassesId) + ".png")

    back.paste(body, (0, 0), body)
    back.paste(ears, (0, 0), ears)
    back.paste(clothes, (0, 0), clothes)
    back.paste(eyes, (0, 0), eyes)
    back.paste(necklace, (0, 0), necklace)
    back.paste(mouth, (0, 0), mouth)
    back.paste(headware, (0, 0), headware)
    if sunglasses:
        back.paste(sunglasses, (0, 0), sunglasses)

    back.save("generatedImages/Bear #" + str(counter) + ".png")

    ipfsHash = dataUpload(counter)

    if sunglasses:
        metadataJsonDict = {
            "Token ID": str(counter),
            "description": "Each Brazen Bear is part of a randomly generated hand-drawn collection. Learn more at brazenbears.io",
            "image": f"https://ipfs.io/ipfs/{ipfsHash}",
            "external_url": "https://www.brazenbears.io",
            "name": f"Bear #{counter}",
            "attributes": [
                {"trait_type": "Body", "value": BodyTags[bodyId]},
                {"trait_type": "Eyes", "value": EyesTags[eyesId]},
                {"trait_type": "Hat", "value": HeadwareTags[headwareId]},
                {"trait_type": "Accessories", "value": EarwareTags[earsId]},
                {"trait_type": "Clothes", "value": ClothesTags[clothesId]},
                {"trait_type": "Background", "value": BackgroundTags[bckId]},
                {"trait_type": "Mouth", "value": MouthTags[mouthId]},
                {"trait_type": "Necklace", "value": NecklaceTags[necklaceId]},
                {"trait_type": "Sunglasses", "value": SunglassesTags[sunglassesId]},
            ],
        }
    else:
        metadataJsonDict = {
            "Token ID": str(counter),
            "description": "Each Brazen Bear is part of a randomly generated hand-drawn collection. Learn more at brazenbears.io",
            "image": f"https://ipfs.io/ipfs/{ipfsHash}",
            "external_url": "https://www.brazenbears.io",
            "name": f"Bear #{counter}",
            "attributes": [
                {"trait_type": "Body", "value": BodyTags[bodyId]},
                {"trait_type": "Eyes", "value": EyesTags[eyesId]},
                {"trait_type": "Hat", "value": HeadwareTags[headwareId]},
                {"trait_type": "Accessories", "value": EarwareTags[earsId]},
                {"trait_type": "Clothes", "value": ClothesTags[clothesId]},
                {"trait_type": "Background", "value": BackgroundTags[bckId]},
                {"trait_type": "Mouth", "value": MouthTags[mouthId]},
                {"trait_type": "Necklace", "value": NecklaceTags[necklaceId]},
            ],
        }

    with open(f"jsonFiles/{counter}.JSON", "w") as json_file:
        json.dump(metadataJsonDict, json_file)
    counter += 1
