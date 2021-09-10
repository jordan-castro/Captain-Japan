#include "pdf.h"
#include <fstream>
#include <filesystem>
#include <string>
#include <iostream>
#include <vector>

vector<string> pdfData;

int main(int argc, char** argv) {
    // Read the data from the data.txt file
    ifstream dataFile(argv[1]);
    string dataHolder;
    // Read
    while(getline(dataFile, dataHolder)) {
        // Add to vector
        pdfData.push_back(dataHolder);
    }
    // Close data file
    dataFile.close();
    // Now instantiate pdf object
    Pdf pdf = Pdf(pdfData[0]);
    // Loop through pdfData starting after 0
    for (int x = 1; x < pdfData.size(); ++x) {
        // Add file
        pdf.addFile(pdfData[x]);
    }
    // Now build pdf
    pdf.build();
}