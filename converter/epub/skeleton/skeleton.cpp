#include "skeleton.h"
#include <string>
#include <fstream>
#include <filesystem>
#include <algorithm>

using namespace std;

EpubSkeleton::EpubSkeleton()
{
}

EpubSkeleton::~EpubSkeleton()
{
}

void EpubSkeleton::buildSkeleton(string epubName)
{
    this->epubName = epubName;
    this->epubPath = "../" + this->epubName;
    // Build the skeleton of the specific epub1
    filesystem::create_directory(this->epubPath);
    filesystem::create_directory(this->epubPath + "/META-INF");
    string obepsPath = this->epubPath + "/OEBPS";
    filesystem::create_directory(obepsPath);
    filesystem::create_directory(obepsPath + "/Images");
    filesystem::create_directory(obepsPath + "/Styles");
    filesystem::create_directory(obepsPath + "/Text");

    this->buildMetaInf();
    this->buildOEPBS();
    this->mimeType();
}

void EpubSkeleton::buildMetaInf()
{
    // The path to the container.
    string containerPath = this->epubPath + "/META-INF/container.xml";
    // Create file object
    ofstream Container(containerPath);
    // Write to Container
    Container << "<?xml version=\"1.0\"?>" << endl;
    Container << "<container version=\"1.0\" xmlns=\"urn:oasis:names:tc:opendocument:xmlns:container\">" << endl;
    Container << "<rootfiles>" << endl;
    Container << "<rootfile full-path=\"OEBPS/content.opf\" media-type=\"application/oebps-package+xml\"/>" << endl;
    Container << "</rootfiles>" << endl;
    Container << "</container>";
    // Cierra
    Container.close();
}

void EpubSkeleton::buildOEPBS()
{
    // The path to the page-template.xpgt
    string pageTemplatePath = this->epubPath + "/OEBPS/Styles/page-template.xpgt";
    // The path to the stylesheet.css
    string styleSheetPath = this->epubPath + "/OEBPS/Styles/stylesheet.css";
    // The path to the contnet.opf
    string contentPath = this->epubPath + "/OEBPS/content.opf";
    // The path to the toc.ncx
    string tableOfContentsPath = this->epubPath + "/OEBPS/toc.ncx";

    // Create page template object
    ofstream PageTemplate(pageTemplatePath);
    PageTemplate << "<ade:template xmlns=\"http://www.w3.org/1999/xhtml\" xmlns:ade=\"http://ns.adobe.com/2006/ade\" ";
    PageTemplate << "xmlns:fo=\"http://www.w3.org/1999/XSL/Format\">\"" << endl;
    PageTemplate << "<fo:layout-master-set>" << endl;
    PageTemplate << "<fo:simple-page-master master-name=\"single_column\">" << endl;
    PageTemplate << "<fo:region-body margin-bottom=\"3pt\" margin-top=\"0.5em\" margin-left=\"3pt\" margin-right=\"3pt\"/>" << endl;
    PageTemplate << "</fo:simple-page-master>" << endl;
    PageTemplate << "<fo:simple-page-master master-name=\"single_column_head\">" << endl;
    PageTemplate << "<fo:region-before extent=\"8.3em\"/>" << endl;
    PageTemplate << "<fo:region-body margin-bottom=\"3pt\" margin-top=\"6em\" margin-left=\"3pt\" margin-right=\"3pt\"/>" << endl;
    PageTemplate << "</fo:simple-page-master>" << endl;
    PageTemplate << "<fo:simple-page-master master-name=\"two_column\" margin-bottom=\"0.5em\" margin-top=\"0.5em\" margin-left=\"0.5em\" margin-right=\"0.5em\">" << endl;
    PageTemplate << "<fo:region-body column-count=\"2\" column-gap=\"10pt\"/>" << endl;
    PageTemplate << "</fo:simple-page-master>" << endl;
    PageTemplate << "<fo:simple-page-master master-name=\"two_column_head\" margin-bottom=\"0.5em\" margin-left=\"0.5em\" margin-right=\"0.5em\">" << endl;
    PageTemplate << "<fo:region-before extent=\"8.3em\"/>" << endl;
    PageTemplate << "<fo:region-body column-count=\"2\" margin-top=\"6em\" column-gap=\"10pt\"/>" << endl;
    PageTemplate << "</fo:simple-page-master>" << endl;
    PageTemplate << "<fo:simple-page-master master-name=\"three_column\" margin-bottom=\"0.5em\" margin-top=\"0.5em\" margin-left=\"0.5em\" margin-right=\"0.5em\">" << endl;
    PageTemplate << "<fo:region-body column-count=\"3\" column-gap=\"10pt\"/>" << endl;
    PageTemplate << "</fo:simple-page-master>" << endl;
    PageTemplate << "<fo:simple-page-master master-name=\"three_column_head\" margin-bottom=\"0.5em\" margin-top=\"0.5em\" margin-left=\"0.5em\" margin-right=\"0.5em\">" << endl;
    PageTemplate << "<fo:region-before extent=\"8.3em\"/>" << endl;
    PageTemplate << "<fo:region-body column-count=\"3\" margin-top=\"6em\" column-gap=\"10pt\"/>" << endl;
    PageTemplate << "</fo:simple-page-master>" << endl;
    PageTemplate << "<fo:page-sequence-master>" << endl;
    PageTemplate << "<fo:repeatable-page-master-alternatives>" << endl;
    PageTemplate << "<fo:conditional-page-master-reference master-reference=\"three_column_head\" page-position=\"first\" ade:min-page-width=\"80em\"/>" << endl;
    PageTemplate << "<fo:conditional-page-master-reference master-reference=\"three_column\" ade:min-page-width=\"80em\"/>" << endl;
    PageTemplate << "<fo:conditional-page-master-reference master-reference=\"two_column_head\" page-position=\"first\" ade:min-page-width=\"50em\"/>" << endl;
    PageTemplate << "<fo:conditional-page-master-reference master-reference=\"two_column\" ade:min-page-width=\"50em\"/>" << endl;
    PageTemplate << "<fo:conditional-page-master-reference master-reference=\"single_column_head\" page-position=\"first\" />" << endl;
    PageTemplate << "<fo:conditional-page-master-reference master-reference=\"single_column\"/>" << endl;
    PageTemplate << "</fo:repeatable-page-master-alternatives>" << endl;
    PageTemplate << "</fo:page-sequence-master>" << endl;
    PageTemplate << "</fo:layout-master-set>" << endl;
    PageTemplate << "<ade:style>" << endl;
    PageTemplate << "<ade:styling-rule selector=\".title_box\" display=\"adobe-other-region\" adobe-region=\"xsl-region-before\"/>" << endl;
    PageTemplate << "</ade:style>" << endl;
    PageTemplate << "</ade:template>" << endl;
    // Cierra
    PageTemplate.close();

    // Ahora creamos el stylesheet
    ofstream StyleSheet(styleSheetPath);
    // Escribe a lo
    StyleSheet << "/* Style Sheet */" << endl;
    StyleSheet << "/* This defines styles and classes used in the book */" << endl;
    StyleSheet << "body { margin-left: 5%; margin-right: 5%; margin-top: 5%; margin-bottom: 5%; text-align: justify; }" << endl;
    StyleSheet << "pre { font-size: x-small; }" << endl;
    StyleSheet << "h1 { text-align: center; }" << endl;
    StyleSheet << "h2 { text-align: center; }" << endl;
    StyleSheet << "h3 { text-align: center; }" << endl;
    StyleSheet << "h4 { text-align: center; }" << endl;
    StyleSheet << "h5 { text-align: center; }" << endl;
    StyleSheet << "h6 { text-align: center; }" << endl;
    StyleSheet << ".CI {" << endl;
    StyleSheet << "text-align:center;" << endl;
    StyleSheet << "margin-top:0px;" << endl;
    StyleSheet << "margin-bottom:0px;" << endl;
    StyleSheet << "padding:0px;" << endl;
    StyleSheet << "}" << endl;
    StyleSheet << ".center   {text-align: center;}" << endl;
    StyleSheet << ".smcap    {font-variant: small-caps;}" << endl;
    StyleSheet << ".u        {text-decoration: underline;}" << endl;
    StyleSheet << ".bold     {font-weight: bold;}" << endl;
    // Cierra
    StyleSheet.close();

    // Ahora el turno de content
    ofstream ContentOpf(contentPath);
    ContentOpf << "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" << endl;
    ContentOpf << "<package xmlns=\"http://www.idpf.org/2007/opf\" unique-identifier=\"BookID\" version=\"2.0\">" << endl;
    ContentOpf << "<metadata xmlns:dc=\"http://purl.org/dc/elements/1.1/\" xmlns:opf=\"http://www.idpf.org/2007/opf\">" << endl;
    ContentOpf << "<dc:title>" << this->epubName << ".epub eBook</dc:title>" << endl;
    ContentOpf << "<dc:language>en</dc:language>" << endl;
    ContentOpf << "<dc:rights>Public Domain</dc:rights>" << endl;
    ContentOpf << "<dc:creator opf:role=\"aut\">Yoda47</dc:creator>" << endl;
    ContentOpf << "<dc:publisher>Jedisaber.com</dc:publisher>" << endl;
    ContentOpf << "<dc:identifier id=\"BookID\" opf:scheme=\"UUID\">015ffaec-9340-42f8-b163-a0c5ab7d0611</dc:identifier>" << endl;
    ContentOpf << "<meta name=\"Sigil version\" content=\"0.2.4\"/>" << endl;
    ContentOpf << "</metadata>" << endl;
    ContentOpf << "<manifest>" << endl;
    ContentOpf << "<item id=\"ncx\" href=\"toc.ncx\" media-type=\"application/x-dtbncx+xml\"/>" << endl;
    // ContentOpf << "<item id=\"sample.png\" href=\"Images/sample.png\" media-type=\"image/png\"/>" << endl;
    // ContentOpf << "<item id=\"page-template.xpgt\" href=\"Styles/page-template.xpgt\" media-type=\"application/vnd.adobe-page-template+xml\"/>" << endl;
    ContentOpf << "<item id=\"stylesheet.css\" href=\"Styles/stylesheet.css\" media-type=\"text/css\"/>" << endl;
    // ContentOpf << "<item id=\"chap01.xhtml\" href=\"Text/chap01.xhtml\" media-type=\"application/xhtml+xml\"/>" << endl;
    // ContentOpf << "<item id=\"chap02.xhtml\" href=\"Text/chap02.xhtml\" media-type=\"application/xhtml+xml\"/>" << endl;
    // ContentOpf << "<item id=\"title_page.xhtml\" href=\"Text/title_page.xhtml\" media-type=\"application/xhtml+xml\"/>" << endl;
    ContentOpf << "</manifest>" << endl;
    ContentOpf << "<spine toc=\"ncx\">" << endl;
    // ContentOpf << "<itemref idref=\"title_page.xhtml\"/>" << endl;
    // ContentOpf << "<itemref idref=\"chap01.xhtml\"/>" << endl;
    // ContentOpf << "<itemref idref=\"chap02.xhtml\"/>" << endl;
    ContentOpf << "</spine>" << endl;
    ContentOpf << "</package>" << endl;
    // Cierra
    ContentOpf.close();

    // Now its toc.ncx turn
    ofstream TOC(tableOfContentsPath);

    TOC << "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" << endl;
    TOC << "<!DOCTYPE ncx PUBLIC \"-//NISO//DTD ncx 2005-1//EN\"" << endl;
    TOC << "\"http://www.daisy.org/z3986/2005/ncx-2005-1.dtd\">" << endl;
    TOC << "<ncx xmlns=\"http://www.daisy.org/z3986/2005/ncx/\" version=\"2005-1\">" << endl;
    TOC << "<head>" << endl;
    TOC << "<meta name=\"dtb:uid\" content=\"015ffaec-9340-42f8-b163-a0c5ab7d0611\"/>" << endl;
    TOC << "<meta name=\"dtb:depth\" content=\"2\"/>" << endl;
    TOC << "<meta name=\"dtb:totalPageCount\" content=\"0\"/>" << endl;
    TOC << "<meta name=\"dtb:maxPageNumber\" content=\"0\"/>" << endl;
    TOC << "</head>" << endl;
    TOC << "<docTitle>" << endl;
    TOC << "<text>Sample .epub eBook</text>" << endl;
    TOC << "</docTitle>" << endl;
    TOC << "<navMap>" << endl;
    TOC << "<navPoint id=\"navPoint-1\" playOrder=\"1\">" << endl;
    TOC << "<navLabel>" << endl;
    TOC << "<text>Sample Book</text>" << endl;
    TOC << "</navLabel>" << endl;
    TOC << "<content src=\"Text/title_page.xhtml\"/>" << endl;
    TOC << "</navPoint>" << endl;
    TOC << "<navPoint id=\"navPoint-2\" playOrder=\"2\">" << endl;
    TOC << "<navLabel>" << endl;
    TOC << "<text>A Sample .epub Book</text>" << endl;
    TOC << "</navLabel>" << endl;
    TOC << "<content src=\"Text/title_page.xhtml#heading_id_3\"/>" << endl;
    TOC << "<navPoint id=\"navPoint-3\" playOrder=\"3\">" << endl;
    TOC << "<navLabel>" << endl;
    TOC << "<text>Title Page</text>" << endl;
    TOC << " </navLabel>" << endl;
    TOC << "<content src=\"Text/title_page.xhtml#heading_id_4\"/>" << endl;
    TOC << " </navPoint>" << endl;
    TOC << "<navPoint id=\"navPoint-4\" playOrder=\"4\">" << endl;
    TOC << "<navLabel>" << endl;
    TOC << "<text>Chapter 1</text>" << endl;
    TOC << " </navLabel>" << endl;
    TOC << "<content src=\"Text/chap01.xhtml\"/>" << endl;
    TOC << " </navPoint>" << endl;
    TOC << "<navPoint id=\"navPoint-5\" playOrder=\"5\">" << endl;
    TOC << "<navLabel>" << endl;
    TOC << "<text>Chapter 2</text>" << endl;
    TOC << " </navLabel>" << endl;
    TOC << "<content src=\"Text/chap02.xhtml\"/>" << endl;
    TOC << " </navPoint>" << endl;
    TOC << " </navPoint>" << endl;
    TOC << " </navMap>" << endl;
    TOC << " </ncx>" << endl;
    // Close
    TOC.close();

    // Build the skeleton html text file.
    ofstream SkeletonText(this->epubPath + "/OEBPS/Text/skeleton.html");
    SkeletonText << "<?xml version=\"1.0\" encoding=\"utf-8\"?>" << endl;
    SkeletonText << "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.1//EN\"" << endl;
    SkeletonText << " \"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd\">" << endl << endl;
    SkeletonText << "<html xmlns=\"http://www.w3.org/1999/xhtml\">" << endl;
    SkeletonText << "<head>" << endl;
    SkeletonText << "  <title>Chapter 1</title>" << endl;
    SkeletonText << "  <link rel=\"stylesheet\" href=\"../Styles/stylesheet.css\" type=\"text/css\" />" << endl;
    SkeletonText << "  <link rel=\"stylesheet\" type=\"application/vnd.adobe-page-template+xml\" href=\"../Styles/page-template.xpgt\" />" << endl;
    SkeletonText << "</head>" << endl << endl;
    SkeletonText << "<body>" << endl;
    SkeletonText << "  <div id=\"body\">" << endl;
    SkeletonText << "    <h3 id=\"heading_id\">Chapter 1</h3>" << endl;
    SkeletonText << "  </div>" << endl << endl;
    SkeletonText << "</body>" << endl;
    SkeletonText << "</html>";
    // Close file
    SkeletonText.close();
}

void EpubSkeleton::mimeType()
{
    // Abre el mimetype
    ofstream MimeType(this->epubPath + "/mimetype");
    // Ahora escribe
    MimeType << "application/epub+zip";
    // Cierra Mist
    MimeType.close();
}

string EpubSkeleton::getName()
{
    return this->epubName;
}

string EpubSkeleton::getPath()
{
    return this->epubPath;
}