import FWCore.ParameterSet.Config as cms

process = cms.Process("SKIM")

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.load("Configuration.StandardSequences.Services_cff")

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )
process.MessageLogger.cerr.FwkReport.reportEvery = 10000

process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring())
process.source.fileNames = [
    '/store/data/Run2012D/DoubleMu/AOD/16Jan2013-v1/10000/FE22C7C3-9B60-E211-A23B-E0CB4E19F99E.root',
]

process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string("skim.root"),
    outputCommands = cms.untracked.vstring("keep *"),
)
process.outPath = cms.EndPath(process.out)

process.load("TopAnalysis.Configuration.commonFilters_cff")
process.load("HLTrigger.HLTfilters.hltHighLevel_cfi")
process.hltHighLevel.throw = False
process.hltHighLevel.HLTPaths = ["HLT_Mu17_Mu8_v*", "HLT_Mu17_TkMu8_v*"]

process.p = cms.Path(
    process.hltHighLevel
  + process.commonSequenceForData
)

