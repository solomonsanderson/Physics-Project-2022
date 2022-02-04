{
//   macro to read xi data from an ascii file and
//   create a root file with an histogram and an ntuple.
   gROOT->Reset();
#include "Riostream.h"

   ifstream in;
// we assume a file Xi.data in the current directory
// this file has 3 columns of float data
   // in.open("mumu-bg.out");
   // in.open("higgs.data");
   in.open("real-dimuon-100k.data");

   Int_t icand;
   Float_t ptL1, phiL1, etaL1, ptL2, phiL2, etaL2, mLL;
   Int_t nlines = 0;
   TFile *f = new TFile("real-data.root","RECREATE");
   // Book histogram (one 1D and one 2D)
   TH1F *effmass = new TH1F("effmass", "dimuon effective mass",100,40.,140.);
   // book ntuples 
  //  TNtuple *ntuple = new TNtuple("ntuple","geometric data","icand:ximass:vmass:v0radius:casradius:cascos:v0cos:dacneg:dcapos:dcabach:dcaV0:dcacas:dcav0");

   while (1) {
      in >> ptL1 >> phiL1 >> etaL1 >> ptL2 >> phiL2 >> etaL2 >> mLL;
      if (!in.good()) break;
      // if (icand < 5) printf("icand=%i, ximass=%8f, vmass=%8fn",icand,ximass,vmass);
      effmass->Fill(mLL);
      nlines++;
      if (nlines < 5) printf("mass=%8f",mLL);
   }
   printf(" found %d pointsn",nlines);

   in.close();

   f->Write();
}
