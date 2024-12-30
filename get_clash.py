import os
import time
import shutil

from utils.yamlUtils import YamlUtils
from utils.cfmem import get_content as cfmem_content
from utils.pawdroid import get_content as pawdroid_content
from utils.NoMoreWalls import get_content as NoMoreWalls_content

# changfengoss = os.path.join("changfengoss")
# dirname = time.strftime("%Y_%m_%d", time.localtime(time.time()))
# yamlUtils = YamlUtils(changfengoss)
# yamlUtils.clone_repo("https://github.com/changfengoss/pub.git")
# yamlUtils.make_template_dict("yaml", dirname)
# yamlUtils.save_file("pub/changfengoss.yaml")
# shutil.rmtree(changfengoss)

cfmem_content()
pawdroid_content()
NoMoreWalls_content()


pub = os.path.join("pub")
yamlUtils = YamlUtils(pub)
yamlUtils.make_template(
    ["cfmem.yaml", "NoMoreWalls.yaml"]
)
yamlUtils.save_file("pub/combine.yaml")
