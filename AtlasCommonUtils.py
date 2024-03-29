#!/usr/bin/env python

# define a function that sets up the ATLAS ROOT style
def SetAtlasStyle():
  from ROOT import TROOT, gROOT, TStyle, gStyle
  atlasStyle = TStyle("ATLAS","Atlas style")
  icol=0
  atlasStyle.SetFrameBorderMode(icol)
  atlasStyle.SetFrameFillColor(icol)
  atlasStyle.SetCanvasBorderMode(icol)
  atlasStyle.SetCanvasColor(icol)
  atlasStyle.SetPadBorderMode(icol)
  atlasStyle.SetPadColor(icol)
  atlasStyle.SetStatColor(icol)
  atlasStyle.SetPaperSize(20,26)
  atlasStyle.SetPadTopMargin(0.05)
  atlasStyle.SetPadRightMargin(0.10)
  atlasStyle.SetPadBottomMargin(0.16)
  atlasStyle.SetPadLeftMargin(0.16)
  atlasStyle.SetTitleXOffset(1.4)
  atlasStyle.SetTitleYOffset(1.4)
  font=42
  tsize=0.05
  atlasStyle.SetTextFont(font)
  atlasStyle.SetTextSize(tsize)
  atlasStyle.SetLabelFont(font,"x")
  atlasStyle.SetTitleFont(font,"x")
  atlasStyle.SetLabelFont(font,"y")
  atlasStyle.SetTitleFont(font,"y")
  atlasStyle.SetLabelFont(font,"z")
  atlasStyle.SetTitleFont(font,"z")
  atlasStyle.SetLabelSize(tsize,"x")
  atlasStyle.SetTitleSize(tsize,"x")
  atlasStyle.SetLabelSize(tsize,"y")
  atlasStyle.SetTitleSize(tsize,"y")
  atlasStyle.SetLabelSize(tsize,"z")
  atlasStyle.SetTitleSize(tsize,"z")
  atlasStyle.SetMarkerStyle(20)
  atlasStyle.SetMarkerSize(1.2)
  atlasStyle.SetHistLineWidth(2)
  atlasStyle.SetLineStyleString(2,"[12 12]")
  atlasStyle.SetEndErrorSize(2)
  atlasStyle.SetOptTitle(0)
  atlasStyle.SetOptStat(0)
  atlasStyle.SetOptFit(0)
  atlasStyle.SetPadTickX(1)
  atlasStyle.SetPadTickY(1)
  gROOT.SetStyle("ATLAS")
  #gROOT.ForceStyle()
  gStyle.SetPalette(1)
