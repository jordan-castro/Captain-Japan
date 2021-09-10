#include "epub.h"
#include <fstream>
#include <sstream>
#include <vector>
#include "skeleton/skeleton.h"
#include <iostream>

Epub::Epub(string epubName)
{
    this->name = epubName;

    EpubSkeleton skeleton = EpubSkeleton();
    skeleton.buildSkeleton(this->name);

    this->path = skeleton.getPath();
}
Epub::~Epub() {}

string Epub::getName()
{
    return this->name;
}

string Epub::getPath()
{
    return this->path;
}

void Epub::addText(string path, string chapterTitle)
{
    // Path to new file
    string xhtmlPath = this->path + "/OEBPS/Text/" + chapterTitle + ".xhtml";
    // Grab data from file being passed
    ifstream htmlFile(path);
    // Read data into variable
    string data;
    string htmlData;
    while (getline(htmlFile, data))
    {
        // Add to htmlData
        htmlData += data;
    }
    // Close htmlfile
    htmlFile.close();
    // We do not need data anymore. Release it's memory
    data.clear();

    // Now open xhtml file
    ofstream xhtmlFile(xhtmlPath);
    // Write to it
    // This is default skeleton data
    xhtmlFile << " <?xml version=\"1.0\" encoding=\"utf-8\"?>" << endl;
    xhtmlFile << "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.1//EN\"" << endl;
    xhtmlFile << " \"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd\">" << endl;
    xhtmlFile << "<html xmlns=\"http://www.w3.org/1999/xhtml\">" << endl;
    xhtmlFile << "<head>" << endl;
    xhtmlFile << "  <title>Chapter 1</title>" << endl;
    xhtmlFile << "  <link rel=\"stylesheet\" href=\"../Styles/stylesheet.css\" type=\"text/css\" />" << endl;
    xhtmlFile << "  <link rel=\"stylesheet\" type=\"application/vnd.adobe-page-template+xml\" href=\"../Styles/page-template.xpgt\" />" << endl;
    xhtmlFile << "</head>" << endl;
    // Start head
    xhtmlFile << "<head>" << endl;
    // Chapter title
    xhtmlFile << "<title>" + chapterTitle + "</title>" << endl;
    // Style sheets
    xhtmlFile << "<link rel=\"stylesheet\" href=\"../Styles/stylesheet.css\" type=\"text/css\" />" << endl;
    xhtmlFile << "<link rel=\"stylesheet\" type=\"application/vnd.adobe-page-template+xml\" href=\"../Styles/page-template.xpgt\" />" << endl;
    // Close head
    xhtmlFile << "</head>" << endl;
    // Write body
    xhtmlFile << "<body>" << endl;
    xhtmlFile << "<div>" << endl;
    xhtmlFile << "<h3 id=\"heading_id\">" + chapterTitle + "</h3>" << endl;
    // This is where the body of the HTMLfile goes
    xhtmlFile << htmlData << endl;
    xhtmlFile << "</div>" << endl;
    // Close body and html
    xhtmlFile << "</body>" << endl;
    xhtmlFile << "</html>";
    // Close file
    xhtmlFile.close();

    // // Grab skeleton path
    // string skeletonPath = this->path + "/OEBPS/Text/skeleton.html";
    // string skeletonLines[18];
    // // Open and convert to array
    // ifstream skeleton(skeletonPath);
    // // Read
    // if (skeleton.is_open()) {
    //     // Put into lines
    //     for (int i = 0; i < 18; i++) {
    //         skeleton >> skeletonLines[i];
    //     }
    // } else {
    //     cout << "Something went wrong" << endl;
    // }
    // // Close
    // skeleton.close();

    // // Now read the html file passed
    // string htmlText;
    // string bodyForPub;

    // ifstream htmlFile(path);
    // // Read data
    // while (getline(htmlFile, htmlText)) {
    //     bodyForPub += (htmlText + "\n");
    // }
    // // Close
    // htmlFile.close();

    // // Now edit skeletonLines
    // skeletonLines[6] = "<title>" + chapterTitle + "</title>\n" ;
    // skeletonLines[13] = "<h3 id=\"heading_id\">" + chapterTitle + "</h3>\n";
    // // Now the lines from the htmlfile
    // skeletonLines[14] = bodyForPub;

    // // Now recreate bodyForPub
    // for (int i = 0; i < 18; i++) {
    //     bodyForPub += skeletonLines[i] + "\n";
    // }

    // // Open new file and write to it.
    // ofstream xhtmlFile(this->path + "/OEBPS/Text/" + chapterTitle + ".xhtml");
    // xhtmlFile << bodyForPub;
    // xhtmlFile.close();
}
void Epub::addImage(string path) {}

void Epub::updateContent() {}
void Epub::updateToc() {}