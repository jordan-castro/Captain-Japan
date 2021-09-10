#include "pdf.h"
#include <fstream>
#include <filesystem>
#include <iostream>

using namespace std;
namespace fs = filesystem;

Pdf::Pdf(string name) {
    this->name = name;
    this->path = "generated_pdfs/" + name;

    fs::create_directory(this->path);

    // Read the amount of files within the path
    for (const auto & entry : fs::directory_iterator(path)) {
        // Add file path to private class vector
        string file = entry.path().string();
        this->currentFiles.push_back(file);
    }
}

Pdf::~Pdf() {}

void Pdf::build() {
    // Check if we have any files to combine.
    if (this->currentFiles.size() >= 1) {
        combineFiles();
    }
    // The command to convert html to pdf
    string command = "wkhtmltopdf " + this->path + "/pdf.html " + "generated_pdfs/" + this->name + ".pdf";
    // Now execute the command line
    system(command.c_str());
    // Now Let's remove the working pdf directory
    fs::remove(this->path + "/pdf.html");
    fs::remove(this->path);
}

void Pdf::addFile(string path) {
    // Lets add the file to the genereated_pdfs path
    // First open file
    ifstream htmlFile(path);
    // Data holder
    string data;
    vector<string> htmlData;

    while (getline(htmlFile, data)) {
        htmlData.push_back(data);
    }
    htmlFile.close();

    string fileForPdfPath = this->path + "/" + to_string(this->currentFiles.size()) + ".html";

    // Now to write the new file.
    ofstream fileForPdf(fileForPdfPath);
    // Write to file
    for (auto str : htmlData) {
        fileForPdf << str << endl;
    }
    // Close file
    fileForPdf.close();

    // Add file path to files
    this->currentFiles.push_back(fileForPdfPath);
}

void Pdf::combineFiles() {
    // The file to write to
    ofstream pdf(this->path + "/pdf.html");
    // Lets loop through the current files
    for (auto filePath : this->currentFiles) {
        // Open the file
        ifstream file(filePath);
        string data;
        // Now write to pdf.html
        while(getline(file, data)) {
            pdf << data;
        }
        file.close();

        try {
            // Remove
            fs::remove(filePath);
        } catch(const fs::filesystem_error) {
            cout << "Could not delete file " << filePath << " from path!" << endl;
            continue;
        }
    }
    pdf.close();
}