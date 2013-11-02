import FWCore.ParameterSet.Config as cms

process = cms.Process("PAT")

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.load("Configuration.StandardSequences.Services_cff")

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )
process.MessageLogger.cerr.FwkReport.reportEvery = 10000

process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring())
process.source.fileNames = [
    '/store/user/jhgoh/MuEG/Run2012A-22Jan2013-v1-KCMSSkim20131027_1/4407ef23eed415918ae815f01ecb7627/skim_1_1_2W6.root',
]

process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string("skim.root"),
    outputCommands = cms.untracked.vstring(
        "keep *",
        "drop *_selectedMuons_*_SKIM",
        "drop *_selectedElectrons_*_SKIM",
        "drop *_z*Cands_*_SKIM",
        "drop *_selectedJets_*_SKIM",
    ),
    SelectEvents = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
)
#process.outPath = cms.EndPath(process.out)

process.load("PhysicsTools.PatAlgos.patSequences_cff")
from PhysicsTools.PatAlgos.tools.pfTools import *

postfix = "PFlow"
jetAlgo="AK5" 
#usePFBRECO(process,runPFBRECO=True, jetAlgo=jetAlgo, runOnMC=True, postfix=postfix) 
usePF2PAT(process,runPF2PAT=True, jetAlgo=jetAlgo, runOnMC=False, postfix=postfix) 

process.p = cms.Path(
    #getattr(process,"patPFBRECOSequence"+postfix) 
    getattr(process,"patPF2PATSequence"+postfix) 
)
