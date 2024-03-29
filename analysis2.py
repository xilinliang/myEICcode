#!/usr/bin/env python

import sys

import ROOT
from AtlasCommonUtils import *
#from Legend import Legend
try:
  input = raw_input
except:
  pass

if len(sys.argv) < 2:
  print(" Usage: Example1.py input_file")
  sys.exit(1)

ROOT.gSystem.Load("libDelphes")

try:
  ROOT.gInterpreter.Declare('#include "classes/DelphesClasses.h"')
  ROOT.gInterpreter.Declare('#include "external/ExRootAnalysis/ExRootTreeReader.h"')
except:
  pass

isCC = False
isNC = False
SetAtlasStyle()

inputFile = sys.argv[1]
if 'CC' in inputFile:
    print 'CC analysis'
    isCC = True
elif 'NC in inputFile':
    print 'NC analysis'
    isNC = True

# Create chain of root trees
chain = ROOT.TChain("Delphes")
chain.Add(inputFile)

# Create object of class ExRootTreeReader
treeReader = ROOT.ExRootTreeReader(chain)
numberOfEntries = treeReader.GetEntries()

# Get pointers to branches used in this analysis
branchParticle = treeReader.UseBranch("Particle")
branchJet = treeReader.UseBranch("Jet")
branchGenJet = treeReader.UseBranch("GenJet")
branchElectron = treeReader.UseBranch("Electron")
branchMet = treeReader.UseBranch("MissingET")
branchGenMet = treeReader.UseBranch("GenMissingET")

##Tracks/Towers
branchTrack = treeReader.UseBranch("Track")
branchTower = treeReader.UseBranch("Tower")
##Particle flow objects
branchEFlowTrack =  treeReader.UseBranch("EFlowTrack")
branchEFlowPhoton = treeReader.UseBranch("EFlowPhoton")
branchEFlowNeutralHadron = treeReader.UseBranch("EFlowNeutralHadron")


# Book histograms
histJetPT = ROOT.TH1F("jet_pt", "jet P_{T}", 100, 0.0, 100.0)

neutral_E = {}
photon_E  = {}
track_E   = {}
for i in range(1,5):
    neutral_E['etabin%i'%i] = ROOT.TH1F("neutral_E_eta%i"%i, "", 100, 0.0, 100.0)
    photon_E['etabin%i'%i]  = ROOT.TH1F("photon_E_eta%i"%i , "" , 100, 0.0,100.0)
    track_E['etabin%i'%i]   = ROOT.TH1F("track_E_eta%i"%i, "", 100, 0.0,100.0)


#Kinematic
y_Matrix = ROOT.TH2F("y_Matrix", "inelasticity response matrix, JB method", 10, 0.0,1.0, 10,0.0,1.0)
x_Matrix = ROOT.TH2F("x_Matrix", "Bjorken x response matrix, JB method", 10, 0.0,1.0, 10,0.0,1.0)
Q2_Matrix = ROOT.TH2F("Q2_Matrix", "Q2 response matrix, JB method", 20, 10,100, 20,10,100) 


## met vs x
Ngen_met_x = ROOT.TH2F("Ngen_met_x", "", 6, 10.0, 40.0, 5, 0.0, 1.0)
Nout_met_x = ROOT.TH2F("Nout_met_x", "", 6, 10.0, 40.0, 5, 0.0, 1.0)
Nin_met_x  = ROOT.TH2F("Nin_met_x", "" , 6, 10.0, 40.0, 5, 0.0, 1.0)

## y vs x 
Ngen_y_x = ROOT.TH2F("Ngen_y_x", "", 5,0.0,1.0, 5, 0.0, 1.0)
Nout_y_x = ROOT.TH2F("Nout_y_x", "", 5,0.0,1.0, 5, 0.0, 1.0)
Nin_y_x  = ROOT.TH2F("Nin_y_x", "" , 5,0.0,1.0, 5, 0.0, 1.0)

## Q2 vs x

import numpy as np
from array import array
binsQ2 = np.logspace(2,4.2,7)
binsx = np.logspace(-2,0,11)
print 'BINS Q2', binsQ2
print 'BINS x ', binsx

Ngen_Q2_x = ROOT.TH2F("Ngen_Q2_x", "", 10, array('d',binsx), 6, array('d',binsQ2))
Nout_Q2_x = ROOT.TH2F("Nout_Q2_x", "", 10, array('d',binsx), 6, array('d',binsQ2))
Nin_Q2_x  = ROOT.TH2F("Nin_Q2_x", "" , 10, array('d',binsx), 6, array('d',binsQ2))




##Diagonal

METMatrix = ROOT.TH2F("METMatrix", "Met Matrix", 30, 10.0, 280.0, 30, 10.0, 280.0)
JetMatrix = ROOT.TH2F("JetMatrix", "Jet Matrix", 100, 10.0, 280.0, 100, 10.0, 280.0)
JetMatrix.SetTitle("smeared jet pT vs jet pT")
JetMatrix.SetXTitle("smeared jet pT (GeV/c)")
JetMatrix.SetYTitle("jet pT (GeV/c)")
JetMatrix.GetXaxis().SetRangeUser(0,280)
JetMatrix.GetYaxis().SetRangeUser(0,280)
ElectronMatrix = ROOT.TH2F("ElectronMatrix", "Electron Matrix", 100,10.0,40.0,100,10.0,40.0)
ElectronMatrix.SetTitle("smeared electron pT vs electron pT")
ElectronMatrix.SetXTitle("smeared electron pT (GeV/c)")
ElectronMatrix.SetYTitle("electron pT (GeV/c)")
ElectronMatrix.GetXaxis().SetRangeUser(0,40)
ElectronMatrix.GetYaxis().SetRangeUser(0,40)

##E vs Eta
Jet_eta_e = ROOT.TH2F("Jet_eta_e", "" , 100,-4.0,4.0, 100, 0, 150.0)





### Jet PT and Phi
minpt = 10
maxpt = 40
nbinspt = 6

profile = {}
ResMatrix = {}
histo = {} 

distribution = {}

##JET, phi, phi
ResMatrix['jetpt'] =    ROOT.TH2F("ResMatrix_jetpt",             "",  nbinspt, minpt, maxpt, 50, -1.0, 1.0)
profile['jetpt'] =      ROOT.TProfile("profile_jetpt",           "",  nbinspt, minpt, maxpt, -1.0,1.0,"s")
ResMatrix['jetphi']  =  ROOT.TH2F("ResMatrix_jetphi" ,           "",  nbinspt, minpt, maxpt, 100, -0.5,0.5)  
profile['jetphi'] =     ROOT.TProfile("profile_jetphi",          "",  nbinspt, minpt, maxpt, -0.5,0.5,"s")

for i in range(1,5):
    ResMatrix['jete_eta%i'%i] = ROOT.TH2F("ResMatrix_jete_eta%i"%i,        "",  20, 10, 200, 50, -1.0,1.0)
    profile['jete_eta%i'%i]   = ROOT.TProfile("profile_jete_eta%i"%i,        "",  20, 10, 200, -1.0, 1.0,"s")

ResMatrix['jete'] = ROOT.TH2F("ResMatrix_jete",        "",  10, 10, 100, 50, -1.0,1.0)
profile['jete']    = ROOT.TProfile("profile_jete", "", 10, 10, 100, -1.0,1.0,"s")
    
### MET PT and Phi
ResMatrix['met']       = ROOT.TH2F("ResMatrix_met",              "", nbinspt, minpt, maxpt, 50, -1.0, 1.0)
profile['met']         = ROOT.TProfile("profile_met",            "", nbinspt, minpt, maxpt, -1.0,1.0,"s")     
ResMatrix['metphi']    = ROOT.TH2F("ResMatrix_metphi",           "", nbinspt, minpt, maxpt, 100, -0.5, 0.5)
profile['metphi']      = ROOT.TProfile("profile_metphi",         "", nbinspt, minpt, maxpt, -0.5, 0.5, "s")

##Electron
ResMatrix['ept'] = ROOT.TH2F("ResMatrix_ept", "", 100, 10.0, 40.0, 100, -.20, .20)
profile['ept']       = ROOT.TProfile("profile_ept", "", 30, 10, 40, -.20,0.20,"s")

ResMatrix['dphi'] = ROOT.TH2F("ResMatrix_dph", "", 6, 10.0, 40.0, 100, -0.5, 0.5)
profile['dphi']  = ROOT.TProfile("profile_dphi", "", 6, 10.0,40.0, -0.5,0.5,"s")
distribution['dphi_reco'] = ROOT.TH2F("distribution_dphi_reco", "",  6, 10.0, 40.0, 20, 2.8, ROOT.TMath.Pi())
distribution['dphi_gen'] = ROOT.TH2F("distribution_dphi_gen", "",  6, 10.0, 40.0, 20, 2.8, ROOT.TMath.Pi())     


ResMatrix['qtnormjet'] = ROOT.TH2F("ResMatrix_qtnormjet", "", 6, 10.0, 40.0, 100, -0.1, 0.1)
profile['qtnormjet']   = ROOT.TProfile("profile_qtnormjet", "", 6, 10.0, 40.0, -0.1, 0.1,"s")
distribution['qtnormjet_reco'] = ROOT.TH2F("distribution_qtnormjet_reco", "",  6, 10.0, 40.0, 20, 0,1.0)
distribution['qtnormjet_gen'] = ROOT.TH2F("distribution_qtnormjet_gen", "",  6, 10.0, 40.0, 20, 0,1.0)

histo['delta_reco'] = ROOT.TH1F("delta_reco","", 100,0.0,30.0)
histo['delta_gen'] = ROOT.TH1F("delta_gen","", 100,0.0,30.0)


h_qt_reco = {}
h_qt_truth = {}

for i in range(1,5):
    h_qt_reco['bin%i'%i] = ROOT.TH1F("qt_reco_bin%i"%i, "qt reco #%i"%i, 20, 0,0.8)
    h_qt_truth['bin%i'%i] = ROOT.TH1F("qt_truth_bin%i"%i, "qt truth #%i"%i, 20, 0,0.8) 

    

ROOT.gStyle.SetOptStat("")
ROOT.gStyle.SetPalette(112)

c = ROOT.TCanvas("c", "c", 800,600)

##JetMatrix.SetTitle("; generated p_{T} [GeV]; reconstructed p_{T} [GeV]")
METMatrix.SetTitle("; generated MET [GeV]; reconstructed MET [GeV]")


ResMatrix['jetpt'].SetTitle("Jet response matrix; p_{T}^{gen} [GeV]; (p_{T}^{reco}-p_{T}^{gen})/p_{T}^{gen}")
ResMatrix['met'].SetTitle("Met response matrix; MET_{T}^{gen} [GeV]; (MET^{reco}-MET^{gen})/MET^{gen}")          
ResMatrix['metphi'].SetTitle(" MET_{T}^{gen} [GeV]; (MET^{reco}-MET^{gen})/MET^{gen}")

Q2_Matrix.SetTitle(" Q^{2} response matrix, JB method ; generated Q^{2} [GeV^{2}]; reconstructed Q^{2} [GeV^{2}]")
x_Matrix.SetTitle(" x response matrix, JB method; generated x; reconstructed x ")
y_Matrix.SetTitle(" y response matrix, JB method; generated y; reconstructed y")

# Loop over all events
for entry in range(0, numberOfEntries):
    #if entry%10000==0:
    #    print 'event ' , entry
    if entry>3000:
       break
    # Load selected branches with data from specified event
    treeReader.ReadEntry(entry)

    # four-momenta of proton, electron, virtual photon/Z^0/W^+-.
    pProton      = branchParticle.At(0).P4(); #these numbers 0 , 3, 5 are hardcoded in Pythia8
    pleptonIn    = branchParticle.At(3).P4();
    pleptonOut   = branchParticle.At(5).P4();
    pPhoton      = pleptonIn - pleptonOut;
  
    #Q2, W2, Bjorken x, y, nu.
    Q2 = -pPhoton.M2()
    W2 = (pProton + pPhoton).M2()
    x = Q2 / (2. * pProton.Dot(pPhoton))
    y = (pProton.Dot(pPhoton)) / (pProton.Dot(pleptonIn))
  
    #Jacquet Blondet method:
    temp = 0
    delta = 0
    temp_p = ROOT.TVector3()
    for i in range(branchEFlowTrack.GetEntries()):
       track_mom = branchEFlowTrack.At(i).P4()
       temp = temp + (track_mom.E() - track_mom.Pz())
       temp_p = temp_p + track_mom.Vect()
     
    for i in range(branchEFlowPhoton.GetEntries()):
       pf_mom = branchEFlowPhoton.At(i).P4()        
       temp = temp + (pf_mom.E() - pf_mom.Pz())
       temp_p = temp_p + pf_mom.Vect() 

    for i in range(branchEFlowNeutralHadron.GetEntries()):
       pf_mom = branchEFlowNeutralHadron.At(i).P4()
       temp = temp + (pf_mom.E() - pf_mom.Pz())
       temp_p = temp_p + pf_mom.Vect()

    delta =  temp
    y_JB   = temp/(2.0*10.0)
    ptmiss = temp_p.Perp()
    Q2_JB  = (ptmiss*ptmiss)/(1-y_JB)
    s     = 4*10.0*275.0
    x_JB  = Q2_JB/(s*y_JB)


#delta at generator level
    gendelta = 0
    for i in range(branchParticle.GetEntries()):
        particle = branchParticle.At(i)
        gen_mom = particle.P4()
        status = particle.Status                       
        if(status!=1): continue            
        gendelta = gendelta + (gen_mom.E() - gen_mom.Pz())                      

    #print 'Gen delta ' , gendelta , ' reco delta ', delta 
    histo['delta_reco'].Fill(delta)
    histo['delta_gen'].Fill(gendelta)










    
    ##Fill purity histograms y-x and Q2-x
    genbin  = Ngen_y_x.FindBin(y, x)
    recobin = Ngen_y_x.FindBin(y_JB,x_JB)
    Ngen_y_x.Fill(y,x)
    if(genbin!=recobin):
        Nout_y_x.Fill(y ,x) ### In a given generator bin, how many left out.
        Nin_y_x.Fill(y_JB, x_JB)
   

    genbin  = Ngen_Q2_x.FindBin(x,Q2)
    recobin = Ngen_Q2_x.FindBin(x_JB,Q2_JB)
    Ngen_Q2_x.Fill(x,Q2)
    if(genbin!=recobin):
        Nout_Q2_x.Fill(x,Q2) ### In a given generator bin, how many left out.
        Nin_Q2_x.Fill(x_JB, Q2_JB)

    x_Matrix.Fill(x, x_JB)
    Q2_Matrix.Fill(ROOT.TMath.Sqrt(Q2), ROOT.TMath.Sqrt(Q2_JB))
    y_Matrix.Fill(y, y_JB)
 
  ## Electron response matrix:
    if branchElectron.GetEntries()>0:
        electron = branchElectron.At(0)
        if branchParticle.GetEntries()>0:
            for i in range(branchParticle.GetEntries()):
                particle = branchParticle.At(i)
                gen_mom = particle.P4()
                pid = particle.PID
                status = particle.Status
                if (pid==11 and status==1 ):
                    gen_electron = particle
                    #print 'electron pT', gen_electron.Pt()
                    ElectronMatrix.Fill(gen_electron.PT, electron.PT)
                    res = (electron.PT-gen_electron.PT)/gen_electron.PT
                    profile['ept'].Fill(gen_electron.PT, res)
                    ResMatrix['ept'].Fill(gen_electron.PT, res)   
                                                                                                                                                                                        
  ##Jet response matrix
    if branchJet.GetEntries() > 0:
        # Take first jet
        jet = branchJet.At(0)

        deltaR = 999
        ipar_best = 999
        for ipar in range(branchGenJet.GetEntries()):
             particle = branchGenJet.At(ipar) #branchParticle.At(ipar)
             genJetMomentum = particle.P4()
             if(genJetMomentum.Px() == 0 and genJetMomentum.Py() == 0): continue

             if(genJetMomentum.DeltaR(jet.P4()) < deltaR):
                 deltaR = genJetMomentum.DeltaR(jet.P4());
                 bestGenJetMomentum = genJetMomentum;
                 ipar_best = ipar
        #print ipar
        #print deltaR
        if (deltaR>0.3): continue
            
        genjet = bestGenJetMomentum #branchGenJet.At(0)
     
        # Print jet transverse momentum
        JetMatrix.Fill( jet.PT*ROOT.TMath.CosH(jet.Eta), genjet.Pt()*ROOT.TMath.CosH(genjet.Eta()))
            
        res = (jet.PT-genjet.Pt())/genjet.Pt()
        profile['jetpt'].Fill(genjet.Pt(), res)
        ResMatrix['jetpt'].Fill(genjet.Pt(),res)
        profile['jetphi'].Fill(genjet.Pt(),   jet.Phi-genjet.Phi())
        ResMatrix['jetphi'].Fill(genjet.Pt(), jet.Phi-genjet.Phi())


        
#       print genjet.PT*ROOT.TMath.CosH(genjet.Eta), ' ',  genjet.P4().E()
        Jet_eta_e.Fill(genjet.Eta(), genjet.Pt()*ROOT.TMath.CosH(genjet.Eta()))
            
        if(genjet.Pt()<10.0):
           continue
        if abs(genjet.Eta())<1.0:
            etabin = 1
        elif genjet.Eta()>1.0 and genjet.Eta()<2.0:
            etabin = 2
        elif genjet.Eta()>2.0 and genjet.Eta()<3.0:
            etabin = 3
        else:
            etabin=4
        ResMatrix['jete_eta%i'%etabin].Fill(genjet.E(), (jet.P4().E()-genjet.E())/genjet.E())
        profile['jete_eta%i'%etabin].Fill(genjet.E(), (jet.P4().E()-genjet.E())/genjet.E())  

        ResMatrix['jete'].Fill(genjet.E(), (jet.P4().E()-genjet.E())/genjet.E())
        profile['jete'].Fill(genjet.E(), (jet.P4().E()-genjet.E())/genjet.E())

    ##Met response matrix
    if branchMet.GetEntries() > 0:
        met = branchMet.At(0)
        genmet = branchGenMet.At(0)
        #print 'MET', met.MET
        #print 'GenMET', genmet.MET
        if branchGenMet.GetEntries()>0:
            METMatrix.Fill(genmet.MET, met.MET)
            res = (met.MET-genmet.MET)/genmet.MET
            profile['met'].Fill(genmet.MET,res)
            ResMatrix['met'].Fill(genmet.MET, res)
            profile['metphi'].Fill(genmet.MET,met.Phi-genmet.Phi)
            ResMatrix['metphi'].Fill(genmet.MET, met.Phi-genmet.Phi)

            ##Fill purity matrices
            ## MET vs x
            genbin = Ngen_met_x.FindBin(genmet.MET, x)
            recobin = Ngen_met_x.FindBin(met.MET,x_JB)
            Ngen_met_x.Fill(genmet.MET,x)
            if(genbin!=recobin):
                Nout_met_x.Fill(genmet.MET,x) ### In a given generator bin, how many left out.
                Nin_met_x.Fill(met.MET, x_JB)
            
    leptonOK = False
    if(isCC and branchMet.GetEntries()>0 and branchGenMet.GetEntries()>0):
        lepton = branchMet.At(0).P4()
        genlepton = branchGenMet.At(0).P4()
        lepton_pt = lepton.Pt()
        genlepton_pt = lepton.Pt()
        leptonOK = True
    elif(isNC and branchElectron.GetEntries()>0):
        lepton = branchElectron.At(0).P4()
        genlepton = branchElectron.At(0).P4()
        lepton_pt = lepton.Pt()
        genlepton_pt = lepton.Pt() 
        leptonOK = True
    ## dphi  
    if leptonOK and branchJet.GetEntries() > 0 and branchGenJet.GetEntries()>0:
        #jet = branchJet.At(0)
        #genjet = branchGenJet.At(0)
        genlepton_phi = genlepton.Phi()
        lepton_phi =    lepton.Phi()
      
        jet_phi =    jet.P4().Phi()
        genjet_phi=  genjet.Phi()
      
        dphi_gen = ROOT.TVector2.Phi_mpi_pi(genlepton_phi-genjet_phi)
        dphi_reco = ROOT.TVector2.Phi_mpi_pi(lepton_phi-jet_phi)

        qT_reco = ROOT.TVector2(jet.P4().Px() + lepton.Px(), jet.P4().Py() + lepton.Py() ).Mod()
        #qT_reco = qT_reco.Mod()/ROOT.TMath.Sqrt(Q2)
      
        qT_truth = ROOT.TVector2(genjet.Px() + genlepton.Px(), genjet.Py() + genlepton.Py() ).Mod()
        #qT_truth = qT_truth.Mod()/ROOT.TMath.Sqrt(Q2)   

        ResMatrix['dphi'].Fill(lepton.Pt(), dphi_reco-dphi_gen)
        profile['dphi'].Fill(lepton.Pt(), dphi_reco-dphi_gen)
        distribution['dphi_gen'].Fill(lepton.Pt(), dphi_gen)
        distribution['dphi_reco'].Fill(lepton.Pt(), dphi_reco)
        
        ResMatrix['qtnormjet'].Fill(lepton.Pt(), qT_reco/jet.PT -qT_truth/genjet.Pt())
        profile['qtnormjet'].Fill(lepton.Pt(), qT_reco/jet.PT -qT_truth/genjet.Pt()) 
        distribution['qtnormjet_reco'].Fill(lepton.Pt(), qT_reco/jet.PT)
        distribution['qtnormjet_gen'].Fill(lepton.Pt(), qT_truth/genjet.Pt())
#####Colors
##for key in profile:
##    profile[key].SetLineColor(2)
##    profile[key].SetLineWidth(2)
##    profile[key].SetMarkerColor(2)
##
##
####Spectrum
##for key in neutral_E.keys():
##    neutral_E[key].SetLineColor(2)
##
##for key in neutral_E.keys():                                                                                                                                                                                          photon_E[key].SetLineColor(4)
##
##for i in range(1,5):
##    neutral_E['etabin%i'%i].Draw()
##    photon_E['etabin%i'%i].Draw("same")
##    track_E['etabin%i'%i].Draw("same")
##    ROOT.gPad.SetLogy(1)
##    c.SaveAs("plots/Spectrum_etabin%i_%s.png"%(i,inputFile))
##    c.SaveAs("plots/Spectrum_etabin%i_%s.pdf"%(i,inputFile))
##
##ROOT.gPad.SetLogy(0)
##
##
##c.Clear()
##METMatrix.Draw("colz")
##c.SaveAs("plots/Diagonal_MET_%s.png"%inputFile)
##c.SaveAs("plots/Diagonal_MET_%s.pdf"%inputFile)
##
##c.Clear()
##JetMatrix.Draw("colz")
##c.SaveAs("plots/Diagonal_Jet_%s.png"%inputFile) 
##c.SaveAs("plots/Diagonal_Jet_%s.pdf"%inputFile)
##
##
##c.Clear()
##y_Matrix.Draw("colz")
##c.SaveAs("plots/y_response_%s.png"%inputFile)
##c.SaveAs("plots/y_response_%s.pdf"%inputFile)
##
##c.Clear()
##x_Matrix.Draw("colz")
##c.SaveAs("plots/x_response_%s.png"%inputFile)
##c.SaveAs("plots/x_response_%s.pdf"%inputFile)
##
##c.Clear()
##
##Q2_Matrix.Draw("colz")
###c.SetLogy(1)
###c.SetLogx(1)
##c.SaveAs("plots/Q2_response_%s.png"%inputFile)
##c.SaveAs("plots/Q2_response_%s.pdf"%inputFile)
##c.SetLogy(0)
##c.SetLogx(0)
##
###input("Press enter to continue...")
##c.Clear()
##ResMatrix['jetpt'].SetTitle("; jet p_{T}^{gen}; (jet p_{T}^{reco} - jet p_{T}^{gen})/jet p_{T}^{gen}")   
##ResMatrix['jetpt'].Draw("colz")
##profile['jetpt'].Draw("same")
##c.SaveAs("plots/profile_jetpt_%s.png"%inputFile)    
##c.SaveAs("plots/profile_jetpt_%s.pdf"%inputFile)
##
####Jet E:
##for i in range(1,4):
##    c.Clear()
##    ResMatrix['jete_eta%i'%i].SetTitle("; jet E^{gen}; (jet E^{reco} - jet E^{gen})/jet E^{gen}")
##    ResMatrix['jete_eta%i'%i].Draw("colz")
##    profile['jete_eta%i'%i].Draw("same")
##    c.SaveAs("plots/profile_jetE_eta%i_%s.png"%(i,inputFile))
##    c.SaveAs("plots/profile_jetE_eta%i_%s.pdf"%(i,inputFile))
##
##
##
###input("Press enter to continue...")
##c.Clear()
##ResMatrix['met'].SetTitle("; generated MET; (MET^{reco} - MET^{gen})/MET^{gen}")
##ResMatrix['met'].Draw("colz")
##profile['met'].Draw("same")
##c.SaveAs("plots/profile_MET_%s.png"%inputFile)
##c.SaveAs("plots/profile_MET_%s.pdf"%inputFile)
##
##c.Clear()
##ResMatrix['metphi'].SetTitle("; generated MET; MET #phi^{reco} - MET #phi^{gen} [rad]")
##ResMatrix['metphi'].Draw("colz")
##profile['metphi'].Draw("same")
##c.SaveAs("plots/profile_METphi_%s.png"%inputFile)
##c.SaveAs("plots/profile_METphi_%s.pdf"%inputFile) 
##
##
##c.Clear()
##ResMatrix['jetphi'].SetTitle("; jet p_{T}^{gen} [GeV]; jet #phi^{reco} - jet #phi^{gen} [rad]")  
##ResMatrix['jetphi'].Draw("colz")
##profile['jetphi'].Draw("same")
##c.SaveAs("plots/profile_jetphi_%s.png"%inputFile) 
##c.SaveAs("plots/profile_jetphi_%s.pdf"%inputFile)  
##
##c.Clear()
##if(isCC):
##    ResMatrix['dphi'].SetTitle("; generated MET; #Delta #phi_{reco} - #Delta #phi_{gen}")
##elif(isNC):
##    ResMatrix['dphi'].SetTitle("; jet p_{T}^{gen} [GeV]; #Delta #phi_{reco} - #Delta #phi_{gen}")
##    
##ResMatrix['dphi'].Draw("colz")
##profile['dphi'].Draw("same")
##c.SaveAs("plots/profile_dphi_%s.png"%inputFile)
##c.SaveAs("plots/profile_dphi_%s.pdf"%inputFile) 
##
##
##c.Clear()
##ResMatrix['qtnormjet'].Draw("colz")
##profile['qtnormjet'].Draw("same")
##c.SaveAs("plots/profile_qtnormjet_%s.png"%inputFile)
##c.SaveAs("plots/profile_qtnormjet_%s.pdf"%inputFile)
##
##if isCC:
##    for i in range(1,7):
##        print 'bin ' , i , ' ' , profile['metphi'].GetBinError(i)
##        print profile['metphi'].GetNbinsX()
##
####projections
##    for i in range(1,7):
##        c.Clear()
##        h = ResMatrix['metphi'].ProjectionY("h",i,i)
##        h.Draw()
##        h.Fit("gaus")
##        f = h.GetFunction("gaus")
##        if(f):
##            f.SetLineColor(2)
##            f.Draw("same")
##            h.Draw("same")
##        c.SaveAs("plots/projection_metphi_%s_%i.png"%(inputFile,i))
##        c.SaveAs("plots/projection_metphi_%s_%i.pdf"%(inputFile,i))
##    
##
##
##
##
##        
##for i in range(1,7):
##    c.Clear()
##    h = ResMatrix['jetphi'].ProjectionY("h",i,i)
##    h.Draw()
##    h.Fit("gaus")
##    f = h.GetFunction("gaus")
##    if(f):
##        f.SetLineColor(2)
##        f.Draw("same")
##        h.Draw("same")
##    c.SaveAs("plots/projection_jetphi_%s_%i.png"%(inputFile,i))
##    c.SaveAs("plots/projection_jetphi_%s_%i.pdf"%(inputFile,i))
##
##for i in range(1,7):
##    c.Clear()
##    h = ResMatrix['dphi'].ProjectionY("h",i,i)
##    h.Draw()
##    h.Fit("gaus")
##    f = h.GetFunction("gaus")
##    if(f):
##        f.SetLineColor(2)
##        f.Draw("same")
##        h.Draw("same")
##    c.SaveAs("plots/projection_dphi_%s_%i.png"%(inputFile,i))            
##
##
##for i in range(1,7):
##    c.Clear()
##    h =ResMatrix['met'].ProjectionY("h",i,i)
##    h.Draw()
##    h.Fit("gaus")
##    f = h.GetFunction("gaus")
##    if(f):
##        f.SetLineColor(2)
##        f.Draw("same")
##        h.Draw("same")
##    c.SaveAs("plots/projection_met_%s_%i.png"%(inputFile,i))
##
##
####Reco vs truth distributions
##    
##for i in range(distribution['dphi_reco'].GetNbinsX()):
##    c.Clear()
##    hgen = distribution['dphi_gen'].ProjectionY("h",i,i).Clone('hgen')
##    hreco  = distribution['dphi_reco'].ProjectionY("h",i,i).Clone('hreco')
##    hgen.SetLineColor(4)    
##    hgen.DrawNormalized()
##    hgen.SetTitle("; | #phi_{lepton} -#phi_{jet} | [rad] ; 1/#sigma d\sigma/d#Delta#phi")
##    hreco.DrawNormalized("same")
##    hreco.SetLineColor(2)
##    c.SaveAs("plots/projection_dphirecogen_%s_%i.png"%(inputFile,i))
##
##for i in range(distribution['qtnormjet_reco'].GetNbinsX()):
##    c.Clear()
##    hgen = distribution['qtnormjet_gen'].ProjectionY("h",i,i).Clone('hgen')
##    hreco  = distribution['qtnormjet_reco'].ProjectionY("h",i,i).Clone('hreco')
##    hgen.SetLineColor(4)
##    hgen.DrawNormalized()
##    hreco.DrawNormalized("same")
##    hreco.SetLineColor(2)
##    c.SaveAs("plots/projection_qtnormjetrecogen_%s_%i.png"%(inputFile,i))
##
##    
##c.Clear()
##Ngen_met_x.Draw("colz")
##c.SaveAs("plots/Ngen_met_x_%s.png"%(inputFile))
##
##
####Purity
##
##ROOT.gStyle.SetPalette(55)
##
##purity_num = Ngen_met_x.Clone("purity_num")
##purity_den = Ngen_met_x.Clone("purity_den")
##print 'Ngen ', Ngen_met_x.GetBinContent(11)
##print 'Nout ', Nout_met_x.GetBinContent(11)
##print 'Nin  ', Nin_met_x.GetBinContent(11)
##purity_num.Add(Nout_met_x,-1)
##purity_den.Add(Nout_met_x,-1)
##purity_den.Add(Nin_met_x)
##purity = purity_num.Clone("purity")
##purity.Divide(purity_den)
##purity.SetMaximum(1.0)
##purity.SetMinimum(0.0)  
##print 'purity ', purity.GetBinContent(11)
##
##c.Clear()
##purity.Draw("colz")
##purity.SetTitle("Purity; reco MET; reco x_{JB}")    
##c.SaveAs("plots/purity_met_x%s.png"%(inputFile))
##c.SaveAs("plots/purity_met_x%s.pdf"%(inputFile))
##
##
##
##
##ROOT.gStyle.SetPalette(112)
##
##c.Clear()
##ROOT.gPad.SetLogy(0)
##ROOT.gPad.SetLogx(0)
##ResMatrix['jete'].Draw("colz")
##ResMatrix['jete'].SetTitle("; jet E^{gen}; (jet E^{reco} - jet E^{gen})/jet E^{gen}")
##profile['jete'].Draw("same")
##c.SaveAs("plots/profile_jetE_%s.png"%(inputFile))
##c.SaveAs("plots/profile_jetE_%s.pdf"%(inputFile))
##
##c.Clear()
##Jet_eta_e.Draw("colz")
##Jet_eta_e.SetTitle("; jet #eta^{gen}; jet E^{gen}")
##c.SaveAs("plots/profile_jetE_eta_%s.png"%(inputFile))
##c.SaveAs("plots/profile_jetE_eta_%s.pdf"%(inputFile))
##
##
##
##
##
##
##
##c.Clear()
##
##histo['delta_reco'].Draw()
##histo['delta_reco'].SetTitle("; #delta ; entries")
##histo['delta_gen'].Draw("same")
##histo['delta_gen'].SetLineColor(2)
##c.SaveAs("plots/delta_%s.png"%(inputFile))
##c.SaveAs("plots/delta_%s.pdf"%(inputFile))
##
##
##
##
##
##
##
##if(isCC):
##    c.Clear()
##
####Purity y vs x 
##    purity_num = Ngen_y_x.Clone("purity_num")
##    purity_den = Ngen_y_x.Clone("purity_den")
##    purity_num.Add(Nout_y_x,-1)
##    purity_den.Add(Nout_y_x,-1)
##    purity_den.Add(Nin_y_x)
##    purity = purity_num.Clone("purity")
##    purity.Divide(purity_den)
##
##    purity.SetMaximum(1.0)
##    purity.SetMinimum(0.0)
##    purity.Draw("colz")
##    purity.SetTitle("Purity; reco x_{JB}; reco y_{JB}")
##    c.SaveAs("plots/purity_y_x_%s.png"%(inputFile))
##    c.SaveAs("plots/purity_y_x_%s.pdf"%(inputFile))
##
##    c.Clear()
####Purity Q2 vs x
##    purity_num = Ngen_Q2_x.Clone("purity_num")
##    purity_den = Ngen_Q2_x.Clone("purity_den")
##    purity_num.Add(Nout_Q2_x,-1)
##    purity_den.Add(Nout_Q2_x,-1)
##    purity_den.Add(Nin_Q2_x)
##    purity = purity_num.Clone("purity")
##
##    purity.Divide(purity_den)
##    purity.SetMaximum(1.0)
##    purity.SetMinimum(0.0)
##    ROOT.gPad.SetLogy(1)
##    ROOT.gPad.SetLogx(1)
##    purity.Draw("colz")
##    purity.SetTitle("Purity; reco x_{JB}; reco Q^{2}_{JB} [GeV^{2}]")
##    c.SaveAs("plots/purity_Q2_x_%s.png"%(inputFile))
##    c.SaveAs("plots/purity_Q2_x_%s.pdf"%(inputFile))

c.Clear()
ElectronMatrix.Draw("colz")
c.SaveAs("plots/ElectronMatrix_%s.png"%(inputFile))
c.SaveAs("plots/ElectronMatrix_%s.jpg"%(inputFile))
c.SaveAs("plots/ElectronMatrix_%s.root"%(inputFile))

c.Clear()
JetMatrix.Draw("colz")
c.SaveAs("plots/JetMatrix_%s.png"%(inputFile))
c.SaveAs("plots/JetMatrix_%s.jpg"%(inputFile))
c.SaveAs("plots/JetMatrix_%s.root"%(inputFile))
