import FWCore.ParameterSet.Config as cms

from CommonTools.RecoAlgos.HBHENoiseFilter_cfi import *

noscraping = cms.EDFilter("FilterOutScraping",
    applyfilter = cms.untracked.bool(True),
    debugOn = cms.untracked.bool(False),
    numtrack = cms.untracked.uint32(10),
    thresh = cms.untracked.double(0.25),
)

goodOfflinePrimaryVertices = cms.EDFilter("PrimaryVertexObjectFilter", 
    src = cms.InputTag('offlinePrimaryVertices'),
    filterParams =  cms.PSet(
        minNdof = cms.double(4.),
        maxZ    = cms.double(24.), 
        maxRho  = cms.double(2.)
    ),
    filter = cms.bool(True),
)

selectedMuons = cms.EDFilter("CandViewSelector",
    src = cms.InputTag("muons"),
    cut = cms.string(
        "abs(eta) < 2.6 && pt > 17"
        " && isPFMuon && (isGlobalMuon || isTrackerMuon)"),
    filter = cms.bool(True),
)

selectedElectrons = cms.EDFilter("CandViewSelector",
    src = cms.InputTag("gsfElectrons"),
    cut = cms.string(
      "abs(eta) < 2.6 && pt > 17"
      " && gsfTrack.isNonnull"
      #" && passConversionVeto "
      " && gsfTrack.trackerExpectedHitsInner.numberOfHits<=0"),
    filter = cms.bool(True),
)

zMuMuCands = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string("selectedMuons@+ selectedMuons@-"),
    checkCharge = cms.bool(False),
    cut = cms.string("10 < mass"),
)

zElElCands = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string("selectedElectrons@+ selectedElectrons@-"),
    checkCharge = cms.bool(False),
    cut = cms.string("10 < mass"),
)

zMuElCands = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string("selectedMuons@+ selectedElectrons@-"),
    checkCharge = cms.bool(False),
    cut = cms.string("10 < mass"),
)

nZMuMuCands = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("zMuMuCands"),
    minNumber = cms.uint32(1),
)
nZElElCands = nZMuMuCands.clone(src = cms.InputTag("zElElCands"))
nZMuElCands = nZMuMuCands.clone(src = cms.InputTag("zMuElCands"))

selectedJets = cms.EDFilter("CandViewSelector",
    src = cms.InputTag("ak5PFJets"),
    cut = cms.string(
        "abs(eta) < 2.6 && pt > 20"
        " && numberOfDaughters > 1"
        " && neutralHadronEnergyFraction < 0.99 && neutralEmEnergyFraction < 0.99"
        " && (abs(eta) >= 2.4 || chargedEmEnergyFraction < 0.99)"
        " && (abs(eta) >= 2.4 || chargedHadronEnergyFraction > 0.)"
        " && (abs(eta) >= 2.4 || chargedMultiplicity > 0)"),
)

nJetFilterSingleLepton = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("selectedJets"),
    minNumber = cms.uint32(3),
)

commonSequenceForData = cms.Sequence(
    goodOfflinePrimaryVertices
  + noscraping
)

commonSequenceForMC = cms.Sequence(
    goodOfflinePrimaryVertices
)

filterDoubleMuSequence = cms.Sequence(
    selectedMuons * zMuMuCands * nZMuMuCands
)

filterDoubleElectronSequence = cms.Sequence(
    selectedElectrons * zElElCands * nZElElCands
)

filterMuEGSequence = cms.Sequence(
    selectedMuons * selectedElectrons * zMuElCands * nZMuElCands
)

filterSingleMuSequence = cms.Sequence(
    selectedMuons
  + selectedJets * nJetFilterSingleLepton
)

filterSingleElectronSequence = cms.Sequence(
    selectedElectrons
  + selectedJets * nJetFilterSingleLepton
)
