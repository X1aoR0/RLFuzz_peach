import numpy as np

from rlfuzz.Peach.Engine.engine import *
from rlfuzz.Peach.Engine.common import *

from rlfuzz.Peach.Analyzers import *
from rlfuzz.Peach.Engine.incoming import DataCracker

import os
import re


class DataModelAnalyse():
    def __init__(self, DataModel):
        #: History of data locations
        self.positions = {}
        #: History of data length
        self.lengths = {}
        # History of data rating
        self.ratings = {}
        # History of data mutebale
        self.mutable = {}

        self.graorder(DataModel)

    def storePosition(self, name, pos):
        """
        Store our position by name
        """
        # print "Storing position of %s at %d" % (name, self.pos)
        self.positions[name] = pos

    def storeRating(self, name, rating):
        """
        Store rating by name
        """
        self.ratings[name] = rating

    def storeLength(self, name, length):
        """
        Store length by name
        """
        self.lengths[name] = length

    def storeMutable(self, name, Mutable):
        """
        Store length by name
        """
        self.mutable[name] = Mutable

    def graorder(self, DataModel_Element):
        if isinstance(DataModel_Element, Empty):
            return None
        ElementQueue = [DataModel_Element]
        while ElementQueue:
            res = []
            for Element in ElementQueue:
                self.storePosition(Element.name, Element.pos)
                self.storeRating(Element.name, Element.rating)
                self.storeLength(Element.name, Element.length)
                self.storeMutable(Element.name, Element.isMutable)
                if Element.hasChildren:
                    for each in Element._children:
                        res.append(each)
            ElementQueue = res

    def Res_Parse(self, DataLength):
        seed_block_start = []
        seed_block = []
        mutate_block_num = []
        unmutate_block_num = []
        for name in self.positions:
            if self.positions[name] not in seed_block_start:
                seed_block_start.append(self.positions[name])
            if self.mutable[name] is True and self.positions[name] not in mutate_block_num:
                mutate_block_num.append(self.positions[name])
            if self.mutable[name] is False and self.positions[name] not in unmutate_block_num:
                unmutate_block_num.append(self.positions[name])
        for each in unmutate_block_num:
            if each in mutate_block_num:
                del mutate_block_num[mutate_block_num.index(each)]
        seed_block_start.sort()
        mutate_block_num.sort()
        for i in range(len(seed_block_start)):
            if i == len(seed_block_start) - 1:
                seed_block.append([seed_block_start[i], DataLength - seed_block_start[i]])
            else:
                seed_block.append([seed_block_start[i], seed_block_start[i + 1] - seed_block_start[i]])
        for i in range(len(mutate_block_num)):
            mutate_block_num[i] = seed_block_start.index(mutate_block_num[i])
        return seed_block, mutate_block_num


def Sample_dataCrack(dataModelName, samplePath, PitPath):
    parser = PitXmlAnalyzer()
    peach = parser.asParser(PitPath)

    # dataModel = peach.templates[dataModelName]

    dataModel = peach.templates[dataModelName].copy(peach)
    with open(samplePath, "rb") as fd:
        data = fd.read()
    buff = PublisherBuffer(None, data, True)
    cracker = DataCracker(peach)
    cracker.optmizeModelForCracking(dataModel, True)
    cracker.crackData(dataModel, buff)
    if dataModel.getValue() == data:
        result = highlight.ok("passed")
    else:
        result = highlight.error("failed")
    logging.info("[%s] cracking: '%s'" % (result, samplePath))
    logging.info("Done.")
    AnalyseResult = DataModelAnalyse(dataModel)
    seed_block, mutate_block_num = AnalyseResult.Res_Parse(len(data))
    return seed_block, mutate_block_num

project_dir = "/home/zzr/RLFuzz_peach"
def NewSample_dataCrack(dataModelName, samplePath, PitPath):
    samplePath = re.sub(r'(&|\*|\?|\||;|~|#|\\)', r'\\\1', samplePath)
    os.system(project_dir+'/rlfuzz/changevenv.sh {} {} {}'.format(dataModelName, samplePath, PitPath))
    if not os.path.exists(project_dir+'/rlfuzz/datacrack_outcome.npy'):
        raise FileExistsError("no model carck data file")
    data_json = np.load(project_dir+'/rlfuzz/datacrack_outcome.npy', allow_pickle=True)
    data = data_json.item()
    seed_block = data['seed_block']
    mutate_block_num = data['mutate_block_num']
    return seed_block, mutate_block_num


if __name__ == '__main__':
    Engine.debug = False
    seed_block, mutate_block_num = NewSample_dataCrack('gzip_file ',
                                                       '/home/real/Rlfuzz-peach/rlfuzz/mods/gzip-mod/seed/switchysharp.rar&1265368&1.exe.gz',
                                                       'file:test/pit/GZIP_DataModel.xml')
    # seed_block, mutate_block_num = NewSample_dataCrack('PNG',
    #                                                    '/home/real/Rlfuzz-peach/rlfuzz/mods/fuzzer-test-suite-mod/libpng-1.2.56/seeds/seed.png',
    #                                                    'file:test/pit/png_datamodel.xml')
