#include "epub.h"
#include <fstream>
#include <sstream>
#include <vector>
#include "skeleton/skeleton.h"
#include <iostream>

Epub::Epub(string epubName) {
    this->name = epubName;

    EpubSkeleton skeleton = EpubSkeleton();
    skeleton.buildSkeleton(this->name);
    
    this->path = skeleton.getPath();
}
Epub::~Epub() {}

string Epub::getName() {
    return this->name;
}

string Epub::getPath() {
    return this->path;
}

void Epub::addText(string path, string chapterTitle) {
    // Grab skeleton path
    string skeletonPath = this->path + "/OEBPS/Text/skeleton.html";
    string skeletonLines[18];
    // Open and convert to array
    ifstream skeleton(skeletonPath);
    // Read
    if (skeleton.is_open()) {
        // Put into lines
        for (int i = 0; i < 18; i++) {
            skeleton >> skeletonLines[i];
        }
    } else {
        cout << "Something went wrong" << endl;
    }
    // Close
    skeleton.close();

    // Now read the html file passed
    string htmlText;
    string bodyForPub;
    
    ifstream htmlFile(path);
    // Read data
    while (getline(htmlFile, htmlText)) {
        bodyForPub += (htmlText + "\n");
    }
    // Close
    htmlFile.close();

    // Now edit skeletonLines
    skeletonLines[6] = "<title>" + chapterTitle + "</title>\n" ;
    skeletonLines[13] = "<h3 id=\"heading_id\">" + chapterTitle + "</h3>\n";
    // Now the lines from the htmlfile
    skeletonLines[14] = bodyForPub;

    // Now recreate bodyForPub
    for (int i = 0; i < 18; i++) {
        bodyForPub += skeletonLines[i] + "\n";
    }

    // Open new file and write to it.
    ofstream xhtmlFile(this->path + "/OEBPS/Text/" + chapterTitle + ".xhtml");
    xhtmlFile << bodyForPub;
    xhtmlFile.close();
}
void Epub::addImage(string path) {}

void Epub::updateContent() {}
void Epub::updateToc() {}