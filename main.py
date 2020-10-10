import sys
import os
import zipfile
import tempfile
from pixivpy3 import *
from PIL import Image


_username = sys.argv[1] 
_password = sys.argv[2]
_illuid = sys.argv[3]

def convert_ugoira(name, metadata):
    with tempfile.TemporaryDirectory() as tmpdirname:

        f = zipfile.ZipFile(name)
        f.extractall(tmpdirname)

        imgList = []
        durationList = []

        for frame in metadata.frames:
            imgList.append(Image.open(os.path.join(tmpdirname,frame.file)))
            durationList.append(frame.delay)

        imgList[0].save(_illuid+".gif", format="GIF", append_images=imgList[1:], duration=durationList, loop=0, save_all=True)
        
        f.close()

        os.remove(name)

    return

def main():

    api = AppPixivAPI()

    api.login(_username, _password)

    json_result = api.illust_detail(_illuid)

    if json_result.illust.type == "ugoira":
        metadata = api.ugoira_metadata(_illuid)
        url = metadata.ugoira_metadata.zip_urls
        api.download(url.medium)

        convert_ugoira(os.path.basename(url.medium), metadata.ugoira_metadata)

    elif json_result.illust.type == "illust":
        for page in json_result.illust.meta_pages:
            api.download(page.image_urls.original)
    else:
        print("Unknonw type : " + json_result.illust.type)

    #print(json_result)

    #api.download(json_result.illust.meta_single_page.original_image_url)

    return

if __name__ == "__main__":
    main()